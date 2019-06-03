{-
  ipu-room plugin market page
-}

module Components.Market exposing (Model, Msg, defaultModel, update, view)

import Browser
import Html exposing (..)
import Html.Events exposing (..)
import Html.Attributes exposing (..)
import Http
import Json.Decode as D exposing (Decoder)
import Json.Decode.Extra exposing (andMap)

-- CSS
import Material
import Material.List as Lists
import Material.Button as Button
import Material.Options as Options
import Material.Icon as Icon

import Components.Page as Page exposing (Page)

-- MODEL
type alias Model m =
  { mdc: Material.Model m
  , packages: List PluginPackage
  , errorMessage: String
  }

defaultModel : Model m
defaultModel =
  { mdc = Material.defaultModel
  , packages = []
  , errorMessage = ""
  }

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

type Msg m
  = Mdc (Material.Msg m)

update : (Msg m -> m) -> Msg m -> Model m -> ( Model m, Cmd m )
update lift msg model =
  case msg of
    Mdc msg_ ->
      Material.update (lift << Mdc) msg_ model

-- VIEW
view : (Msg m -> m) -> Page m -> Model m -> Html m
view lift page model =
  page.body "List"
    "Lists present multiple line items vertically as a single continuous element."
    [ Page.pages 
      [ viewPackages lift model "sample"
      ]
    ]

-- show packages list or error message
viewPackages : (Msg m -> m) -> Model m -> Material.Index -> Html m
viewPackages lift model index =
  Lists.ul (lift << Mdc) index model.mdc
    (Lists.twoLine :: Lists.avatarList :: demoList lift model index)
    [ Lists.divider [] []
    ]

demoList : (Msg m -> m) -> Model m -> Material.Index -> List (Lists.Property m)
demoList lift model index = 
  []

-- returns repos list elements
-- viewPackage : PluginPackage -> Lists.ListItem m
-- viewPackage r =
--   Lists.li []
--     [ Lists.graphicIcon demoIcon "folder"
--     , Lists.text []
--       [ Lists.primaryText [] [ text r.name ]
--       , Lists.secondaryText [] [ text r.description ]
--       ]
--     , Lists.metaIcon [] "info"
--     ]

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