async function loadComponent(
    elementId,
    file
){

    const response =
        await fetch(
            `../components/${file}`
        );

    const html =
        await response.text();

    document
        .getElementById(elementId)
        .innerHTML = html;

}