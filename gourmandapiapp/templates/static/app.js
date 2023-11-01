
console.log("ronald here");
link_rv = document.querySelector('[data-id="resend-verification-link"]');
link_rv.addEventListener(
  "click",
  (eve) => {
    window.alert('A new verification email has been sent to you by email :D')
    console.log(eve)
  }
);