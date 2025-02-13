const body = document.querySelector("body"),
    toggleSidebar = body.querySelector(".toggle-sidebar"),
    sidebar = body.querySelector(".sidebar"),
    main = body.querySelector("main"),
    tag = body.querySelector(".tag");
// cards = body.querySelector(".cards"),
cardElements = body.querySelectorAll(".card");

toggleSidebar.addEventListener("click", () => {
    sidebar.classList.toggle("close");
    main.classList.toggle("scale");
    tag.classList.toggle("scale");
    // cards.classList.toggle("scale");
    cardElements.forEach(card => {
        card.classList.toggle("scale");
    });
});