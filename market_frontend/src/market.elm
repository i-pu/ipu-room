{-
  ipu-room plugin market page
-}

import Browser
import Html exposing (..)
import Html.Events exposing (..)
import Html.Attributes exposing (..)
import Http
import Json.Decode as D exposing (Decoder)
import Json.Decode.Extra exposing (andMap)
-- CSS
import Bootstrap.Form as Form
import Bootstrap.Form.Input as Input
import Bootstrap.Button as Button
import Bootstrap.ListGroup as ListGroup
import Bootstrap.Alert as Alert
import Bootstrap.Badge as Badge

main =
  Browser.element
    { init = init
    , update = update
    , view = view
    , subscriptions = \_ -> Sub.none
    }

-- MODEL
type alias PluginPackage =
  { name: String
  , id: String
  , version: String
  , thumbnail_url: String
  , description: String
  , author: String
  , tags: String
  , requirements: String
  , last_updated: String
  , published: Bool
  , content: String
  }

type alias Model =
  { packages: List PluginPackage
  , errorMessage: String
  }

init : () -> ( Model, Cmd Msg )
init _ = 
  ( { packages = []
    , errorMessage = ""
    }
  , Cmd.none
  )

-- UPDATE
type Msg
  = OnClick
  | Recieve (Result Http.Error (List PluginPackage))

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case msg of
    OnClick ->
      ( model
      , Http.get
        { url = "http://localhost:3000/plugins/"
        , expect = Http.expectJson Recieve packagesDecoder
        }
      )

    Recieve (Ok r) ->
      ( { model | packages = r }, Cmd.none )
    Recieve (Err error) ->
      ( { model | errorMessage = Debug.toString error }, Cmd.none )
-- VIEW
view : Model -> Html Msg
view model =
  div []
    [ Form.formInline []
      [ Button.button
          [ Button.primary
          , Button.onClick OnClick
          , Button.attrs
            [ class "ml-sm-2 my-2"
            ]
          ]
          [ text "Get" ]
      ]
    , viewResult model
    ]

-- show packages list or error message
viewResult : Model -> Html msg
viewResult model =
  if model.errorMessage == "" then
    ListGroup.ul (List.map viewPackage model.packages)
  else
    Alert.simpleDanger [] [ text model.errorMessage ]

-- returns repos list elements
viewPackage : PluginPackage -> ListGroup.Item msg
viewPackage r =
  ListGroup.li []
    [ h3 [ class "lead" ]
      [ text r.name
      , Badge.badgeSecondary [ class "ml-2" ] [ text r.version ]
      ]
    ]

-- DATA
packageDecoder : Decoder PluginPackage
packageDecoder =
  -- ( D.maybe ( D.field "language" D.string ))
  D.succeed PluginPackage
    |> andMap ( D.field "name" D.string )
    |> andMap ( D.field "id" D.string )
    |> andMap ( D.field "version" D.string )
    |> andMap ( D.field "thumbnail_url" D.string )
    |> andMap ( D.field "description" D.string )
    |> andMap ( D.field "author" D.string )
    |> andMap ( D.field "tags" D.string )
    |> andMap ( D.field "requirements" D.string )
    |> andMap ( D.field "last_updated" D.string )
    |> andMap ( D.field "published" D.bool )
    |> andMap ( D.field "content" D.string )

packagesDecoder : Decoder (List PluginPackage)
packagesDecoder =
  D.list packageDecoder