it('should GET consult using consult_id', () => {
  // Locate the div with the class 'opblock-summary opblock-summary-put' containing the specified text
  cy.get('.opblock-summary.opblock-summary-put')
    .contains('Update consult')
    .click(); // Click the div itself

  // Click on the 'Try it out' button
  cy.get('.btn.try-out__btn').click();

  // Set the `consult_id` parameter
  cy.get('input[type="text"][placeholder="consult_id"]').clear().type('3');

  // Set the required body parameter(s)
  cy.get('textarea[name="body"]').clear().type(JSON.stringify({ "param1": "value1", "param2": "value2" }));

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
