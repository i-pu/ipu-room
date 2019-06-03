module Main exposing (main)

import Browser
import Browser.Navigation

-- import Store.Url exposing (ToolbarPage(..), TopAppBarPage(..))
import Html exposing (Html, p, text, div)
import Material
import Material.Options as Options exposing (cs, css, styled)
-- import Material.TopAppBar as TopAppBar
import Material.Typography as Typography

import Components.Page
import Components.Url
import Components.Market

import Url

type alias Model =
  { mdc : Material.Model Msg
  , key : Browser.Navigation.Key
  , url : Components.Url.Url
  , market : Components.Market.Model Msg
  }

defaultModel : Browser.Navigation.Key -> Model
defaultModel key =
  { mdc = Material.defaultModel
  , key = key
  , url = Components.Url.Marketpage
  , market = Components.Market.defaultModel
  }

type Msg
  = Mdc (Material.Msg Msg)
  | Navigate Components.Url.Url
  | UrlRequested Browser.UrlRequest
  | UrlChanged Url.Url
  | MarketMsg (Components.Market.Msg Msg)

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case msg of
    Mdc msg_ -> 
      Material.update Mdc msg_ model

    Navigate url ->
      ( { model | url = url }
      , Cmd.batch
        [ Browser.Navigation.pushUrl model.key (Components.Url.toString url)
        ]
      )

    UrlRequested (Browser.Internal url) ->
      ( { model | url = Components.Url.fromUrl url }
      , Browser.Navigation.load (Components.Url.toString (Components.Url.fromUrl url))
      )

    UrlRequested (Browser.External string) ->
      ( model, Cmd.none )

    UrlChanged url ->
      ( { model | url = Components.Url.fromUrl url }, Cmd.none )

    MarketMsg msg_ ->
      let
        ( market, effects ) =
          Components.Market.update MarketMsg msg_ model.market
      in
      ( { model | market = market }, effects )

view : Model -> Browser.Document Msg
view model =
  { title = "Market"
  , body = [ view_ model ]
  }

view_ : Model -> Html Msg
view_ model =
  let
    page =
      { navigate = Navigate
      , body =
        \title intro nodes ->
          div [] nodes
      }
  in
    case model.url of
      Components.Url.Marketpage ->
        Components.Market.view MarketMsg page model.market
      Components.Url.Error404 requestedHash ->
        div []
          [ Options.styled Html.h1
            [ Typography.display4
            ]
            [ text "404" ]
          , text requestedHash
        ]

main : Program () Model Msg
main =
  Browser.application
    { init = init
    , view = view
    , subscriptions = subscriptions
    , update = update
    , onUrlRequest = UrlRequested
    , onUrlChange = UrlChanged
    }

init : () -> Url.Url -> Browser.Navigation.Key -> ( Model, Cmd Msg )
init _ url key =
  let
    initialModel = defaultModel key
  in
    ( { initialModel | url = Components.Url.fromUrl url }
    , Material.init Mdc
    )

-- SUBSCRIPTIONS
subscriptions : Model -> Sub Msg
subscriptions model =
  Material.subscriptions Mdc model