// import Cookies from "js-cookie";
import { USER_AUTHOR_ID_COOKIE } from "../../src/constants";

describe('e2e tests', () => {
  it('can login and logout', () => {
    cy.clearCookie(USER_AUTHOR_ID_COOKIE);

    cy.visit('http://127.0.0.1:5173/')

    cy.get("h1").should("contain", "InstaTonne")

    cy.get("input#input-0").type("username1")

    cy.get("input#input-2").type("password1")

    cy.contains("Login").click()
    
    cy.get("#homeHeader").should("contain", "Your Stream")

    cy.getCookie(USER_AUTHOR_ID_COOKIE).should("have.property", "value", "1")

    cy.contains("Logout").trigger("mouseover").click()

    cy.getCookie(USER_AUTHOR_ID_COOKIE).should("equal", null)

    cy.visit('http://127.0.0.1:5173/')

    cy.get("h1").should("contain", "InstaTonne")

    cy.clearCookie(USER_AUTHOR_ID_COOKIE);
  })
})