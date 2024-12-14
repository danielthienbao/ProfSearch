async function searchProfessor() {
    const professorName = document.getElementById('professorName').value;

    if (!professorName) {
        alert('Please enter a professor name!');
        return;
    }

    try {
        // Fetch data from API
        const response = await fetch(`http://localhost:5000/search?name=${encodeURIComponent(professorName)}`);

        if (!response.ok) {
            throw new Error('Failed to fetch professor details');
        }

        const data = await response.json();

        // Display results
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = `
            <p><strong>Name:</strong> ${data.name}</p>
            <p><strong>RateMyProfessor Grade:</strong> ${data.rmpGrade}</p>
            <p><strong>RateMyProfessor Link:</strong> <a href="${data.rmpLink}" target="_blank">${data.rmpLink}</a></p>
            <p><strong>Grade Distribution:</strong></p>
            <ul>
                ${data.gradeDistribution.map(grade => `<li>${grade.grade}: ${grade.count}</li>`).join('')}
            </ul>
        `;

        document.getElementById('resultContainer').style.display = 'block';
    } catch (error) {
        alert('Error: ' + error.message);
    }
}
