describe('API Manage Endpoint Testing', () => {
    // Define the base URL of your FastAPI application
    const baseUrl = 'https://backendfinal-eta.vercel.app';
  
    beforeEach(() => {
      // Visit the Swagger UI page
      cy.visit(`${baseUrl}/docs#/`);
    });

it('should UPDATE specific medicine in tha table', () => {
    // Locate the div with the class 'opblock-summary opblock-summary-put' containing the specified text
    cy.get('.opblock-summary.opblock-summary-put')
      .contains('Update Medicine')
      .click(); // Click the div itself
  
    // Click on the 'Try it out' button
    cy.get('.btn.try-out__btn').click();
    
    // Locate all 'parameters-col_description' containers and iterate through each one
    cy.get('.parameters-col_description').first();

    // Set the `consult_id` parameter
    cy.get('input[type="text"][placeholder="medicine_ID"]').clear().type('2');

                cy.get('input[type="text"][placeholder="nurseID"]').clear().type('1');

                // Locate the course input field and enter a value
                cy.get('input[type="text"][placeholder="brandName"]').clear().type('test');

                // Locate the student last name input field and enter a value
                cy.get('input[type="text"][placeholder="drugName"]').clear().type('test');

                // Locate the student first name input field and enter a value
                cy.get('input[type="text"][placeholder="expiration"]').clear().type('02/23/2030');

                // Locate the student first name input field and enter a value
                cy.get('input[type="text"][placeholder="quantity"]').clear().type('10');
  
    // Execute the endpoint
    cy.get('.btn.execute').click();
  
    cy.wait(5000);

    // Wait for the response to be visible and check that it's not empty
    cy.get('.response')
      .find('.response-body') // Adjust selector as necessary
      .should('not.be.empty');
  
    // Check for possible errors
    cy.get('.response')
      .find('.microlight')
      .should('not.contain', 'Internal Server Error')
      .and('not.contain', 'Error');
  });
});