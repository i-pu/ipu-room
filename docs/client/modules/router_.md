[Ipu-space](../README.md) > ["router"](../modules/router_.md)

# External module: "router"

## Index

### Variables

* [router](router_.md#router)

---

## Variables

<a id="router"></a>

### `<Const>` router

**● router**: *`VueRouter`* =  new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Top',
      component: Top,
    },
    {
      path: '/lobby',
      name: 'Lobby',
      component: Lobby,
    },
    {
      path: '/room/:roomId',
      name: 'Room',
      component: Room,
    },
  ],
})

*Defined in [router.ts:13](https://github.com/i-pu/ipu/blob/ce338ba/client/src/router.ts#L13)*

___

