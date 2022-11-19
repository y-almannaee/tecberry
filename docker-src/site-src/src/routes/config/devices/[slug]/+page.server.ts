// from https://kit.svelte.dev/docs/routing#page
import { error } from '@sveltejs/kit';
 
/** @type {import('./$types').PageLoad} */
export function load({ params }) {
  console.log(params)
    return {
      name: 'Example Device',
	  id: parseInt(params.slug),
      desc: 'Example description of the device, its position, pins etc',
	  public: [],
	  private: [],
    }
}