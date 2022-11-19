import { writable } from "svelte/store";
import { localStorageStore } from "@brainandbones/skeleton";

export const definitions = writable({});
export const instances = writable({});

export const user = localStorageStore('user', { name: 'Unknown User', pfp: null, rank: 0 });

import { createClient } from 'redis';
const client = createClient();

client.on('error', (err) => console.log("Redis client error", err));
await client.connect();
export const redis_client = client;