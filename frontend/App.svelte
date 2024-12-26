<script lang="ts">
    import PrinterSelection from "./lib/PrinterSelection.svelte";
    import Printer from "./lib/Printer.svelte";
    import { RouterView } from "@dvcol/svelte-simple-router/components";
    import { ModeWatcher } from "mode-watcher";

    import Sun from "lucide-svelte/icons/sun";
    import Moon from "lucide-svelte/icons/moon";

    import { toggleMode } from "mode-watcher";
    import { Button } from "$lib/components/ui/button/index.js";

    import type { Route, RouterOptions } from "@dvcol/svelte-simple-router/models";

    let { children } = $props();

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
<ModeWatcher />
{@render children?.()}

<Button onclick={toggleMode} variant="outline" size="icon">
    <Sun class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
    <Moon class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
    <span class="sr-only">Toggle theme</span>
</Button>
