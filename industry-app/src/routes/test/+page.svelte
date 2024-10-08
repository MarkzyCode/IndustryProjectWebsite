<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Social Media Platform</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>

    <!-- Banner Section -->
    <header class="banner">
        <div class="banner-content">
            <h1>Welcome to SocialConnect</h1>
            <p>Stay connected with your friends and the world around you.</p>
            <a href="#signup" class="cta-button">Get Started</a>
        </div>
    </header>

    <section id="signup">
        <h2>Join Our Community</h2>
        <p>Sign up and stay connected!</p>
    </section>

</body>

<style>
    /* General Reset */
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
  
    /* Body Style */
    body {
      font-family: 'Arial', sans-serif;
      color: #333;
      background-color: #f4f4f9;
      line-height: 1.6;
    }
  
    /* Banner Style */
    .banner {
      background: linear-gradient(to right, #ff5f6d, #ffc371);
      color: white;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      text-align: center;
      padding: 0 20px;
    }
  
    .banner-content h1 {
      font-size: 3.5rem;
      margin-bottom: 1rem;
      letter-spacing: 1.5px;
    }
  
    .banner-content p {
      font-size: 1.2rem;
      margin-bottom: 2rem;
      max-width: 600px;
    }
  
    .cta-button {
      display: inline-block;
      padding: 15px 30px;
      font-size: 1.2rem;
      color: white;
      background-color: #ff5f6d;
      border: none;
      border-radius: 50px;
      text-decoration: none;
      transition: background-color 0.3s ease-in-out;
    }
  
    .cta-button:hover {
      background-color: #ff8474;
    }
  
    /* Section Style */
    #signup {
      padding: 50px;
      text-align: center;
    }
  
    #signup h2 {
      font-size: 2rem;
      margin-bottom: 1rem;
    }
  
    #signup p {
      font-size: 1.2rem;
    }
  </style>