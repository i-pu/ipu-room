// https://docs.cypress.io/api/introduction/api.html

describe('Top test', () => {
  it('Visits the Top', () => {
    cy.visit('/')
  })

  it('Go to Lobby', () => {
    cy.visit('/')
    cy.get('input').type('あああ')
    cy.contains('Lobby').click()
  })
})

describe('Lobby test', () => {
  it('Create room', () => {
    cy.visit('/')
    cy.get('input').type('あああ')
    cy.contains('Lobby').click()
    cy.get(':nth-child(4) > .layout > .v-btn').click()
    cy.get('input').first().type('へや1')
    cy.get('.v-select__selections').click()
    cy.get('.v-list__tile__title').click()
    cy.get('button').contains('作成').click()
  })
})
