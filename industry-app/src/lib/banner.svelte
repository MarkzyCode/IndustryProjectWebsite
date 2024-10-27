<link rel="stylesheet" type="text/css" href="./src/styles.css"/>

<script>
  let isOpen = false;
  let showDropdown = false;

  const toggleMenu = () => {
    if (!isOpen) {
      showDropdown = true; // Show the dropdown immediately
      isOpen = true; // Set isOpen to true to apply the open class
    } else {
      isOpen = false; // Set isOpen to false immediately
      setTimeout(() => {
        showDropdown = false; // Delay hiding the dropdown to allow animation to complete
      }, 300); // Match the timeout to your CSS transition duration
    }
  };

  import { onMount } from 'svelte';

    let isFading = false; // Track if fading is in progress
    let showText = true; // Track visibility of the text

    function checkWidth() {
        if (window.innerWidth <= 850) {
            // Start the fade-out process if the width is less than or equal to 800px
            if (showText) {
                isFading = true; // Trigger fading animation
                setTimeout(() => {
                    showText = false; // Hide the text after the fade-out transition
                }, 1000); // Match this duration to your CSS transition duration
            }
        } else {
            // Reset to show the text if width is greater than 800px
            isFading = false;
            showText = true;
        }
    }

    onMount(() => {
        // Initial check when the component mounts
        checkWidth();

        // Set up the resize event listener
        window.addEventListener('resize', checkWidth);

        // Clean up the event listener on component destroy
        return () => {
            window.removeEventListener('resize', checkWidth);
        };
    });

    if (typeof window !== 'undefined' && window.innerWidth <= 800) {
        showText = false; // Hide the text immediately if the condition is met
    }

</script>

<div class="navbar">
    <img src="/turtlepic.png" alt="Turtle Logo" class="navbar__logo">
    <div>
        <h1 class="navbar__projectname">TRAC</h1>
        <h1 class="navbar__projectname">Application</h1>
    </div>
   
    <div class="navbar__container--secondary">
      {#if showText}
        <h1 class="navbar__menulabel {!showText ? 'fade-out' : ''}">Menu</h1>
      {/if}
      <div class="navbar__icon {isOpen ? 'open' : ''}" on:click={toggleMenu}>
          <span></span>
          <span></span>
          <span></span>
      </div>

      <div class="navbar__dropdown {isOpen ? 'open' : ''}" style:visibility={showDropdown ? 'visible' : 'hidden'}>
          <a href="/"><i class="fa-solid fa-house"></i>Home Page</a>
          <a href="/login"><i class="fa-solid fa-user"></i>Login</a>
          <a href="/results">Results</a>
      </div>
    </div>
    
</div>