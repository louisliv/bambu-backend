<script lang="ts">
    import Printer from "./lib/Printer.svelte";
    import { RouterView } from "@dvcol/svelte-simple-router/components";

    import type { Route, RouterOptions } from "@dvcol/svelte-simple-router/models";
    import Dashboard from "./lib/Dashboard.svelte";
    import Navbar from "./lib/Navbar.svelte";
    import { Toaster } from "$lib/components/ui/sonner";

    const RouteName = {
        Home: "home",
        Printer: "printer",
        Dashboard: "selection",
        Any: "any",
    } as const;

    type RouteNames = (typeof RouteName)[keyof typeof RouteName];

    export const routes: Readonly<Route<RouteNames>[]> = [
        {
            name: RouteName.Home,
            path: "/",
            component: Dashboard,
        },
        {
            name: RouteName.Printer,
            path: "/printer",
            component: Printer,
        },
    ];

    export const options: RouterOptions<RouteNames> = {
        routes,
    } as const;
</script>

<Navbar />
<Toaster />
<RouterView {options} />
