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
</script>

<div class="navbar">
    <img src="/turtlepic.png" alt="Turtle Logo" class="navbar__logo">
    <div>
        <h1 class="navbar__projectname">TRAC</h1>
        <h1 class="navbar__projectname">Application</h1>
    </div>
   
    <h1 class="navbar__menulabel">Menu</h1>

    <div class="navbar__icon {isOpen ? 'open' : ''}" on:click={toggleMenu}>
        <span></span>
        <span></span>
        <span></span>
    </div>

    <div class="navbar__dropdown {isOpen ? 'open' : ''}" style:visibility={showDropdown ? 'visible' : 'hidden'}>
        <a href="/">Home</a>
        <a href="/details">Login</a>
        <a href="/results">About Us</a>
        <a href="/services">[Insert Client Company Website]</a>
    </div>
</div>