<script lang="ts">
    import GitHubButton from "$lib/GitHubButton.svelte";
    import ModeToggleButton from "$lib/ModeToggleButton.svelte";

    import { link } from "@dvcol/svelte-simple-router/router";
    import { getBackendUrl } from "$lib/utils.js";

    import { onMount } from "svelte";

    const ACTIVE_NAV = "text-primary font-medium";
    const NON_ACTIVE_NAV = "text-muted-foreground font-medium hover:text-primary";

    let printers = $state<string[]>([]);

    let url = getBackendUrl();

    onMount(async () => {
        try {
            const response = await fetch(url + "/api/printers");
            if (!response.ok) throw new Error("Failed to fetch printers");
            printers = await response.json();
        } catch (error) {
            console.error("Error fetching printers:", error);
        }
    });
</script>

<div class="sticky top-0 z-50 w-full border-b bg-background shadow-sm">
    <div class="container mx-auto flex h-16 items-center px-4">
        <nav class="flex items-center space-x-4 lg:space-x-6">
            <a href="/" use:link class={NON_ACTIVE_NAV}> Dashboard </a>
        </nav>

        <div class="ml-auto flex items-center space-x-4">
            <ModeToggleButton />
            <a href="https://github.com/fidoriel/BambUI" target="_blank"> <GitHubButton /></a>
        </div>
    </div>
</div>
