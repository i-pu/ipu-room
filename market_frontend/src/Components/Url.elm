module Components.Url exposing
  ( Url(..)
  , fromString
  , fromUrl
  , toString
  )

import Url

type Url
  = Marketpage
  | Error404 String

-- type ToolbarPage
--   = DefaultToolbar

-- type TopAppBarPage
--   = StandardTopAppBar

toString : Url -> String
toString url =
  -- let
    -- toolbarCase toolbar =
    --   case toolbar of
    --     Nothing ->
    --       "#toolbar"
    --     Just DefaultToolbar ->
    --       "#toolbar/default-toolbar"

    -- topAppBarCase topAppBar =
    --   case topAppBar of
    --     Nothing ->
    --       "#top-app-bar"

    --     Just StandardTopAppBar ->
    --       "#top-app-bar/standard"
  -- in
    case url of
      Marketpage -> "#"
      Error404 requestedHash -> requestedHash

fromUrl : Url.Url -> Url
fromUrl url =
    fromString (Maybe.withDefault "" url.fragment)

fromString : String -> Url
fromString url =
  case url of
    "" -> Marketpage
    -- "toolbar" ->
    --     Toolbar Nothing
    -- "toolbar/default-toolbar" ->
    --     Toolbar (Just DefaultToolbar)
    -- "top-app-bar" ->
    --     TopAppBar Nothing
    -- "top-app-bar/standard" ->
    --     TopAppBar (Just StandardTopAppBar)
    _ -> Error404 url