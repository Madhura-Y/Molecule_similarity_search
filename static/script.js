async function searchMolecule() {

    const query = document.getElementById("query").value;

    const response = await fetch("/search", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            query: query
        })
    });

    const data = await response.json();

    const resultsDiv = document.getElementById("results");

    resultsDiv.innerHTML = "";

    if (data.status === "success") {

        data.results.forEach((item, index) => {

            resultsDiv.innerHTML += `

                <div class="card">

                    <h3>Rank ${index + 1}</h3>

                    <p><b>ID:</b> ${item.id}</p>

                    <p><b>Similarity:</b>
                        ${item.similarity.toFixed(4)}
                    </p>

                    <p><b>SMILES:</b>
                        ${item.smiles}
                    </p>

                </div>
            `;
        });

    } else {

        resultsDiv.innerHTML =
            `<p>${data.message}</p>`;
    }
}