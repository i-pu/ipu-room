{-------------------------------
  Page.elm
  - page layout component

  Copyright (c) 2019 i-pu
---------------------------------}

module Components.Page exposing (Page, pages)

import Html exposing (Html, div, h2, text)
import Html.Attributes as Html

-- CSS
import Material
import Material.Typography as Typography
-- import Material.Icon as Icon
import Material.Options as Options exposing (Property, cs, css, styled)

import Components.Url exposing (Url)

-- Page
type alias Page m =
  { navigate : Url -> m
  , body : String -> String -> List (Html m) -> Html m
  }

pages : List (Html m) -> Html m
pages nodes =
  div [] (
    styled h2 [ Typography.headline6 ] [ text "Demos" ]
    :: nodes
  )

-- toolbar :
--   (Material.Msg m -> m)
--   -> Material.Index
--   -> Material.Model m
--   -> (Url -> m)
--   -> Url
--   -> String
--   -> Html m
-- toolbar lift idx mdc navigate url title =
--   TopAppBar.view lift
--     idx
--     mdc [ ]
--     [ TopAppBar.section
--       [ TopAppBar.alignStart
--       ]
--       [ styled Html.div
--         []
--         [ case url of
--             Url.StartPage ->
--               styled Html.img
--               [] []

--             _ ->
--               Icon.view
--               []
--               "arrow_back"
--         ]
--         , TopAppBar.title
--           []
--           [ text title ]
--         ]
--       ]

-- header : String -> Html m
-- header title =
--   styled Html.h1
--     [ Typography.headline5 ]
--     [ text title ]

-- subheader : String -> Html m
-- subheader title =
--   styled Html.h3
--     [ Typography.subtitle1 ]
--     [ text title ]

-- hero : List (Property c m) -> List (Html m) -> Html m
-- hero options =
--     styled Html.section []