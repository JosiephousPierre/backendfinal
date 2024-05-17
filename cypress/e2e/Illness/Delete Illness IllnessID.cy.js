// File: cypress/integration/api_manage.spec.js

describe('API Manage Endpoint Testing', () => {
    // Define the base URL of your FastAPI application
    const baseUrl = 'https://backendfinal-eta.vercel.app';
  
    beforeEach(() => {
      // Visit the Swagger UI page
      cy.visit(`${baseUrl}/docs#/`);
    });
  
    it('should DELETE illness on table using illness_Id', () => {
      // Locate the div with the class 'opblock-summary opblock-summary-get' and contains the specified text
      cy.get('.opblock-summary.opblock-summary-delete')
      .contains('Delete Illness')
      .click(); // Click the div itself
  
      // Once on the redirected URL, locate the 'Try it out' button and click it
      cy.get('.btn.try-out__btn').click();

      // Locate all 'parameters-col_description' containers and iterate through each one
      cy.get('.parameters-col_description').first();

      // Locate the nurseID input field and enter a value between 1-5
      cy.get('input[type="text"][placeholder="illness_Id"]').clear().type('2');
  
      // Locate the 'Execute' button and click it
      cy.get('.btn.execute').click();

      cy.wait(5000);
  
      // Wait for the response body to be visible and check if it's not empty
      cy.get('.response')
        .find('.response-body') // Adjust selector as necessary
        .should('not.be.empty');
  
      // Optionally, you can check the response body content if necessary
      cy.get('.response')
        .find('.microlight')
        .should('not.contain', 'Internal Server Error')
        .and('not.contain', 'Error');
    });
  });
  