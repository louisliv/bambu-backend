<script lang="ts">
    import PrinterSelection from "./lib/PrinterSelection.svelte";
    import Printer from "./lib/Printer.svelte";
    import { RouterView } from "@dvcol/svelte-simple-router/components";

    import type { Route, RouterOptions } from "@dvcol/svelte-simple-router/models";

    const RouteName = {
        Home: "home",
        Printer: "printer",
        Selection: "selection",
        Any: "any",
    } as const;

    type RouteNames = (typeof RouteName)[keyof typeof RouteName];

    export const routes: Readonly<Route<RouteNames>[]> = [
        {
            name: RouteName.Home,
            path: "/",
            redirect: {
                name: RouteName.Selection,
            },
        },
        {
            name: RouteName.Selection,
            path: "/printers",
            component: PrinterSelection,
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

<RouterView {options} />
