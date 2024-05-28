document.addEventListener("DOMContentLoaded", () => {
    const checkbox = document.getElementById("checkbox");

    // Function to set a cookie
    function setCookie(name, value, days) {
      const d = new Date();
      d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
      const expires = "expires=" + d.toUTCString();
      document.cookie = name + "=" + value + ";" + expires + ";path=/";
    }

    // Function to get a cookie
    function getCookie(name) {
      const nameEQ = name + "=";
      const ca = document.cookie.split(';');
      for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
      }
      return null;
    }

    // Check the cookie on page load
    const darkMode = getCookie("darkMode");
    if (darkMode === "enabled") {
      document.documentElement.classList.add("dark");
      checkbox.checked = true;
    } else {
      document.documentElement.classList.remove("dark");
      checkbox.checked = false;
    }

    // Add event listener to toggle dark mode
    checkbox.addEventListener("change", () => {
      if (checkbox.checked) {
        document.documentElement.classList.add("dark");
        setCookie("darkMode", "enabled", 7); // Cookie expires in 7 days
      } else {
        document.documentElement.classList.remove("dark");
        setCookie("darkMode", "disabled", 7); // Cookie expires in 7 days
      }
    });
  });