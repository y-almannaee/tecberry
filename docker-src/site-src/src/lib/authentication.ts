import {writable} from "svelte/store";

export const user = writable(localStorage.user ? localStorage.getItem("user") : null);

