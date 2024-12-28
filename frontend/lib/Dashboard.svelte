<script lang="ts">
    import { onMount } from "svelte";
    import { link } from "@dvcol/svelte-simple-router/router";
    import { getBackendUrl } from "$lib/utils.js";
    import { Card } from "$lib/components/ui/card";
    import { Button } from "$lib/components/ui/button";
    import { Axis3D } from "lucide-svelte";
    import { Skeleton } from "$lib/components/ui/skeleton";

    let printers: string[] = [];

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

<div class="container mx-auto p-4">
    <h1 class="mb-6 text-3xl font-bold">Available Printers</h1>

    <div class="grid gap-4">
        {#if printers.length > 0}
            {#each printers as printer}
                <Card>
                    <a
                        href="/printer?printerId={printer}"
                        use:link
                        class="flex items-center gap-4 p-4 transition-colors hover:bg-muted"
                    >
                        <Axis3D class="h-5 w-5 text-muted-foreground" />
                        <div class="flex-1">
                            <h3 class="font-semibold">{printer}</h3>
                        </div>
                        <Button variant="ghost" size="sm">View Details →</Button>
                    </a>
                </Card>
            {/each}
        {:else}
            <Card>
                <div class="p-4">
                    <Skeleton class="mb-2 h-4 w-48" />
                    <Skeleton class="h-4 w-32" />
                </div>
            </Card>
            <Card>
                <div class="p-4">
                    <Skeleton class="mb-2 h-4 w-48" />
                    <Skeleton class="h-4 w-32" />
                </div>
            </Card>
        {/if}
    </div>
</div>
