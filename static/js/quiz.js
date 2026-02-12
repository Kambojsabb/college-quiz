document.addEventListener("visibilitychange", function() {
    if (document.hidden) {
        alert("Warning! Do not switch tab.");
        fetch("/tab-warning/", {method: "POST",
        headers: {
            "X-CSRFToken": "{{ csrf_token }}"
        }});
    }
});

