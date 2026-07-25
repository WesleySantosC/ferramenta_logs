async function getLogs(params = "") {

    const response = await fetch(
        `${API}/logs${params}`
    );

    return await response.json();
}

async function getStats() {

    const response = await fetch(`${API}/logs/stats`);

    return await response.json();

}