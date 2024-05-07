// File: cypress/integration/api_manage.spec.js

describe('API Manage Endpoint Testing', () => {
    // Define the base URL of your FastAPI application
    const baseUrl = 'https://backendfinal-eta.vercel.app';
  
    beforeEach(() => {
        // Visit the Swagger UI page
        cy.visit(`${baseUrl}/docs#/`);
    });

    it('should CREATE illness on the table', () => {
        // Locate the div with the class 'opblock-summary opblock-summary-post' that contains the specified text
        cy.get('.opblock-summary.opblock-summary-post')
            .contains('/api/manage_illness/')
            .click(); // Click to expand the endpoint

        // Once the endpoint is expanded, locate the 'Try it out' button and click it
        cy.get('.btn.try-out__btn').click();

        // Locate all 'parameters-col_description' containers and iterate through each one
        cy.get('.parameters-col_description').first();

                // Locate the course input field and enter a value
                cy.get('input[type="text"][placeholder="nurseID"]').clear().type('1');

                // Locate the student last name input field and enter a value
                cy.get('input[type="text"][placeholder="illness"]').clear().type('test');

                
        // After setting the inputs, locate the 'Execute' button and click it
        cy.get('.btn.execute').click();

        cy.wait(5000);

         // Wait for the response body (with class "microlight" and code class "language-json") to be visible
        cy.get('.microlight code.language-json') // Wait up to 10 seconds
        .should('exist') // Ensure the element exists
        .should('not.be.empty') // Check that the element is not empty
        .then(($responseCode) => {
            // You can inspect the text within the response body
            const responseText = $responseCode.text();

            // Check that the response text does not contain internal server errors or errors
            expect(responseText).to.not.include('Internal Server Error');
            expect(responseText).to.not.include('Error');

            // Optionally, you can add more assertions to check specific values within the responseText
            // For example:
            // expect(responseText).to.include('expected value');
        });
});
}); 