// import Cookies from "js-cookie";
import { USER_AUTHOR_ID_COOKIE } from "../../src/constants";

describe('e2e tests', () => {
  it('can login and logout', () => {
    // continue testing in case another call fails
    cy.on('uncaught:exception', (err, runnable) => {
      return false
    })

    cy.clearCookie(USER_AUTHOR_ID_COOKIE);

    cy.visit('http://127.0.0.1:5173/')

    cy.get("h1").should("contain", "InstaTonne")

    cy.get("input#input-0").type("username1")

    cy.get("input#input-2").type("password1")

    cy.contains("Login").click()
    
    cy.get("#homeHeader").should("contain", "Your Stream")

    cy.getCookie(USER_AUTHOR_ID_COOKIE).should("have.property", "value", "1")

    cy.get(".mdi-logout").trigger("mouseover").click()

    cy.get(".confirmButton").click()

    cy.getCookie(USER_AUTHOR_ID_COOKIE).should("equal", null)

    cy.visit('http://127.0.0.1:5173/')

    cy.get("h1").should("contain", "InstaTonne")

    cy.clearCookie(USER_AUTHOR_ID_COOKIE);
  })

  it('can create new post', () => {
    // continue testing in case another call fails
    cy.on('uncaught:exception', (err, runnable) => {
      return false
    })

    cy.clearCookie(USER_AUTHOR_ID_COOKIE);

    cy.visit('http://127.0.0.1:5173/')  

    cy.get("h1").should("contain", "InstaTonne")

    cy.get("input#input-0").type("username1")

    cy.get("input#input-2").type("password1")

    cy.contains("Login").click()
    
    cy.get("#homeHeader").should("contain", "Your Stream")

    cy.getCookie(USER_AUTHOR_ID_COOKIE).should("have.property", "value", "1")
    
    cy.get(".mdi-plus").trigger("mouseover").click()

    cy.get(".mdi-plus").trigger("mouseleave")

    // enter post info
    cy.get("#TitleInput").type("TestTitle")

    cy.get("#ContentInput").type("TestContent")

    cy.get("#DescriptionInput").type("TestDescription")

    cy.get("#VisibilitySelector").parent().click()

    cy.contains("PUBLIC").click()

    cy.get("#SaveButton").click()

    cy.get("#homeHeader").should("contain", "Your Stream")
  })

  it('can edit post', () => {
    cy.clearCookie(USER_AUTHOR_ID_COOKIE);

    cy.visit('http://127.0.0.1:5173/')  

    cy.get("h1").should("contain", "InstaTonne")

    cy.get("input#input-0").type("username1")

    cy.get("input#input-2").type("password1")

    cy.contains("Login").click()
    
    cy.get("#homeHeader").should("contain", "Your Stream")

    // we need to go direct cause the JS Cookie doesn't get updated
    cy.visit('http://127.0.0.1:5173/ProfilePage/1')

    // continue testing in case we don't have any followers
    cy.on('uncaught:exception', (err, runnable) => {
      return false
    })

    // view test post
    cy.contains("TestTitle").click()

    cy.get(".mdi-pencil-outline").click()

    cy.get("#TitleInput").type("UPDATED")

    cy.get("#SaveButton").click()

    cy.go("back")

    cy.go("back")

    cy.get("#TitleText").should("contain", "UPDATED")
  })

  it('can follow user', () => {
    cy.clearCookie(USER_AUTHOR_ID_COOKIE);

    cy.visit('http://127.0.0.1:5173/')  

    cy.get("h1").should("contain", "InstaTonne")

    cy.get(".UsernameField").type("username2")

    cy.get(".PasswordField").type("password2")

    cy.contains("Login").click()
    
    cy.get("#homeHeader").should("contain", "Your Stream")

    cy.get(".mdi-account-search").trigger("mouseover").click()

    cy.get(".mdi-account-search").trigger("mouseleave")

    // continue testing in case we don't have any followers
    cy.on('uncaught:exception', (err, runnable) => {
      return false
    })

    // view user page
    cy.contains("displayName1").click()

    cy.get("h1").should("contain", "displayName1")

    cy.get(".FollowButton").click()

    cy.contains("Follow request sent to user!")

    cy.get(".mdi-logout").trigger("mouseover").click()

    cy.get(".confirmButton").click()

    cy.getCookie(USER_AUTHOR_ID_COOKIE).should("equal", null)

    // Login as followed user
    cy.get("h1").should("contain", "InstaTonne")

    cy.get(".UsernameField").type("username1")

    cy.get(".PasswordField").type("password1")

    cy.contains("Login").click()

    cy.get("#homeHeader").should("contain", "Your Stream")

    cy.get(".mdi-account-group").trigger("mouseover").click()

    cy.get(".mdi-account-group").trigger("mouseleave")

    cy.contains("displayName2")
  })
})