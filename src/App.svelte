<style>
  main {
    font-family: "Avant Garde", sans-serif;
    text-align: left;
    padding: 0 1em;
    max-width: 240px;
    margin: 0 auto;
  }

  h1 {
    color: #ff3366;
    font-size: xx-large;
    font-weight: 100;
  }

  h1,
  h2 {
    font-family: "Futura Book", sans-serif;
    text-transform: uppercase;
    line-height: 1em;
    margin-bottom: 0.2em;
  }

  h2 {
	  font-size: x-large;
  }

  h3 {
    display: inline;
    font-size: larger;
    font-weight: 400;
  }

  h3:after {
    content: "\a";
    white-space: pre;
  }

  p {
	  font-size: large;
  }

  .slide {
    height: 100vh;
    width: 100%;
  }

  .heading {
    margin-bottom: 24px;
  }

  @media (min-width: 640px) {
    main {
      max-width: 80vw;
    }
  }
</style>

<script lang="ts">
  import HelloCube from "./HelloCube.svelte";
  import Logo from "./Logo.svelte";

  export let name: string;
</script>

<Logo />
<main>
  <div class="slide">
    <span class="heading">
      <h1>
        TEC modules for rapid and automated thermomechanical fatigue testing
      </h1>
      <h3>
        By M. Kamal, M. Abu Shaqra, and Y. AlMannaee <br /> Advised by Dr. M. Alkhader
      </h3>
    </span>
    <p>The introduction goes here.</p>
  </div>
  <div class="slide">
    <span class="heading">
      <h2>What is a TEC module?</h2>
    </span>
    <p>
      A TEC module, also known as a thermoelectric, or a Peltier module, is
      basically a heat pump.
    </p>
  </div>
  <HelloCube />
</main>
