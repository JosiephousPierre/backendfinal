// File: cypress/integration/api_manage.spec.js

describe('API Manage Endpoint Testing', () => {
    // Define the base URL of your FastAPI application
    const baseUrl = 'https://backendfinal-eta.vercel.app';
  
    beforeEach(() => {
      // Visit the Swagger UI page
      cy.visit(`${baseUrl}/docs#/`);
    });
  
    it('should GET all the medicine in the table', () => {
      // Locate the div with the class 'opblock-summary opblock-summary-get' and contains the specified text
      cy.get('.opblock-summary.opblock-summary-get')
        .contains('/api/manage_med/')
        .click(); // Click the div itself
  
      // Cypress should now navigate to the specific URL: /docs#/Manage/read_manage_api_manage__get
  
      // Once on the redirected URL, locate the 'Try it out' button and click it
      cy.get('.btn.try-out__btn').click();
  
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
  