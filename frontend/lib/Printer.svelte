<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { useRoute } from "@dvcol/svelte-simple-router/router";
    import { getBackendUrl } from "$lib/utils.js";

    import { Card, CardContent } from "$lib/components/ui/card";
    import { Button } from "$lib/components/ui/button";
    import { Slider } from "$lib/components/ui/slider";
    import { Home } from "lucide-svelte";
    import { Progress } from "$lib/components/ui/progress";
    import { AspectRatio } from "$lib/components/ui/aspect-ratio";
    import { Fan } from "lucide-svelte";
    import { CirclePause } from "lucide-svelte";
    import { CirclePlay } from "lucide-svelte";
    import { CircleStop } from "lucide-svelte";
    import { Lightbulb } from "lucide-svelte";
    import { CircleGauge, Activity } from "lucide-svelte";
    import { File, Layers, Clock, Thermometer } from "lucide-svelte";

    import { Label } from "$lib/components/ui/label/index.js";
    import { Switch } from "$lib/components/ui/switch/index.js";

    const speedModes = ["Silent", "Standard", "Sport", "Ludicrous"];

    const { route, location, routing } = useRoute();
    const queryParams = $derived(location.query);
    const printerId = queryParams["printerId"];

    let imageUrl = $state<string | null>(null);
    let ws = $state<WebSocket | null>(null);
    let connectionError = $state<string | null>(null);

    function connect() {
        const backendUrl = getBackendUrl();
        ws = new WebSocket(`${backendUrl}/ws/printer/${printerId}`);

        ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            if (message.type === "jpeg_image") {
                const binaryData = atob(message.data);
                const bytes = new Uint8Array(binaryData.length);
                for (let i = 0; i < binaryData.length; i++) {
                    bytes[i] = binaryData.charCodeAt(i);
                }
                const blob = new Blob([bytes], { type: "image/jpeg" });

                if (imageUrl) {
                    URL.revokeObjectURL(imageUrl);
                }
                imageUrl = URL.createObjectURL(blob);
            }
        };

        ws.onerror = (error) => {
            connectionError = "Connection error occurred";
            console.error("WebSocket error:", error);
        };

        ws.onclose = (event) => {
            if (event.code === 4004) {
                connectionError = "Invalid printer name";
            }
        };
    }

    onMount(() => {
        connect();
    });

    onDestroy(() => {
        if (ws) {
            ws.close();
        }
        if (imageUrl) {
            URL.revokeObjectURL(imageUrl);
        }
    });

    // placeholders
    let status = "Printing";
    let fileName = "Ergo_Vertical_Mouse_V2_Left_and_Right_Handed";
    let layer = 83;
    let totalLayers = 631;
    let timeRemaining = "2h55m";
</script>

<div class="grid grid-flow-row-dense auto-rows-min grid-cols-1 gap-4 p-4 md:grid-cols-5">
    <div class="flex flex-col space-y-4 md:col-span-3">
        <!-- Camera Feed -->
        <div class="w-full">
            <AspectRatio ratio={16 / 9}>
                {#if connectionError}
                    <div>{connectionError}</div>
                {:else if imageUrl}
                    <img src={imageUrl} alt="Printer camera feed" class="h-full w-full rounded-md object-cover" />
                {:else}
                    <div>Connecting to printer camera...</div>
                {/if}
            </AspectRatio>
        </div>

        <!-- Print Status -->
        <Card class="bg-900">
            <CardContent class="p-4">
                <div class="flex flex-row items-center space-x-8">
                    <!-- File Name -->
                    <div class="flex flex-col items-start">
                        <span class="text-sm text-gray-400"><File /></span>
                        <span class="text-sm font-medium">{fileName}</span>
                    </div>

                    <!-- Status -->
                    <div class="flex flex-col items-start">
                        <span class="text-sm text-gray-400"><Activity /></span>
                        <span class="text-sm font-medium">{status}</span>
                    </div>

                    <!-- Layer Info -->
                    <div class="flex flex-col items-start">
                        <span class="text-sm text-gray-400"><Layers /></span>
                        <span class="text-sm font-medium">{layer}/{totalLayers}</span>
                    </div>

                    <!-- Time Remaining -->
                    <div class="flex flex-col items-start">
                        <span class="text-sm text-gray-400"><Clock /></span>
                        <span class="text-sm font-medium">{timeRemaining}</span>
                    </div>

                    <Progress value={42} max={100} />
                </div>

                <div class="mt-4 flex flex-row items-center justify-between space-x-4">
                    <h3 class="text-lg">Printing 42%</h3>
                    <CirclePause />
                    <CircleStop />
                    <CirclePlay />
                </div>
            </CardContent>
        </Card>
    </div>
    <div class="flex flex-col space-y-4 md:col-span-2">
        <div class="flex items-center justify-between">
            <h1 class="text-2xl font-bold">{printerId}</h1>
        </div>
        <!-- Move Controls (Upper Right) -->
        <Card class="bg-900">
            <CardContent class="p-2">
                <div class="flex flex-col justify-center gap-4 md:flex-row md:gap-8">
                    <!-- XY Controls -->
                    <div class="flex flex-col gap-2">
                        <!-- Y+ Controls -->
                        <div class="flex justify-center">
                            <div class="flex flex-col gap-2">
                                <Button variant="outline" class="w-16">Y+10</Button>
                                <Button variant="outline" class="w-16">Y+1</Button>
                            </div>
                        </div>

                        <!-- X Controls -->
                        <div class="flex gap-2">
                            <Button variant="outline" class="w-16">X-10</Button>
                            <Button variant="outline" class="w-16">X-1</Button>
                            <Button variant="outline" class="w-16">
                                <Home class="h-4 w-4" />
                            </Button>
                            <Button variant="outline" class="w-16">X+1</Button>
                            <Button variant="outline" class="w-16">X+10</Button>
                        </div>

                        <!-- Y- Controls -->
                        <div class="flex justify-center">
                            <div class="flex flex-col gap-2">
                                <Button variant="outline" class="w-16">Y-1</Button>
                                <Button variant="outline" class="w-16">Y-10</Button>
                            </div>
                        </div>
                    </div>

                    <!-- Z and Filament Controls -->
                    <div class="flex gap-8">
                        <!-- Z Controls -->
                        <div class="flex flex-col gap-2">
                            <Button variant="outline" class="w-16">Z+10</Button>
                            <Button variant="outline" class="w-16">Z+1</Button>
                            <Button variant="outline" class="w-16">Z-1</Button>
                            <Button variant="outline" class="w-16">Z-10</Button>
                        </div>

                        <!-- Filament Controls -->
                        <div class="flex flex-col gap-2">
                            <Button variant="outline" class="w-16">Retract</Button>
                            <Button variant="outline" class="w-16">Extrude</Button>
                            <Button variant="outline" class="w-16">Load</Button>
                            <Button variant="outline" class="w-16">Unload</Button>
                        </div>
                    </div>
                </div>
                <div class="mt-6 grid grid-cols-1 gap-4">
                    <div class="bg-400 rounded-lg p-3">
                        <div class="mb-2 flex justify-between">
                            <div class="flex items-center space-x-4">
                                <CircleGauge />
                                Speed
                            </div>
                            <span>Normal</span>
                        </div>
                        <Slider value={[1]} max={3} step={1} class="w-full" />
                    </div>
                </div>
            </CardContent>
        </Card>

        <!-- Chamber Controls (Lower Right) -->
        <Card class="space-y-6">
            <CardContent class="p-4">
                <div class="grid grid-cols-4 gap-4">
                    <div class="flex flex-col items-center justify-center space-y-1">
                        <div class="text-400 flex items-center justify-center space-x-2 text-sm">
                            <Thermometer /> Nozzle
                        </div>
                        <div class="text-center text-xl">42°C</div>
                    </div>
                    <div class="flex flex-col items-center justify-center space-y-1">
                        <div class="text-400 flex items-center justify-center space-x-2 text-sm">
                            <Thermometer /> Bed
                        </div>
                        <div class="text-center text-xl">24°C</div>
                    </div>
                    <div class="flex flex-col items-center justify-center space-y-1">
                        <div class="text-400 flex items-center justify-center space-x-2 text-sm">
                            <Thermometer /> Chamber
                        </div>
                        <div class="text-center text-xl">23°C</div>
                    </div>
                    <div class="flex items-center justify-center space-x-2">
                        <Switch id="printer-light" />
                        <Label for="printer-light">
                            <Lightbulb class="h-5 w-5" />
                        </Label>
                    </div>
                </div>

                <div class="mt-6 grid grid-cols-1 gap-4">
                    <div class="bg-400 rounded-lg p-3">
                        <div class="mb-2 flex justify-between">
                            <div class="flex items-center space-x-4">
                                <Fan />
                                Part Cooling
                            </div>
                            <span>42%</span>
                        </div>
                        <Slider value={[42]} max={100} step={5} class="w-full" />
                    </div>
                    <div class="bg-400 rounded-lg p-3">
                        <div class="mb-2 flex justify-between">
                            <div class="flex items-center space-x-4">
                                <Fan />
                                Chamber
                            </div>
                            <span>42%</span>
                        </div>
                        <Slider value={[42]} max={100} step={5} class="w-full" />
                    </div>
                    <div class="bg-400 rounded-lg p-3">
                        <div class="mb-2 flex justify-between">
                            <div class="flex items-center space-x-4">
                                <Fan />
                                Auxillary
                            </div>
                            <span>42%</span>
                        </div>
                        <Slider value={[42]} max={100} step={5} class="w-full" />
                    </div>
                </div>
            </CardContent>
        </Card>
    </div>
</div>
