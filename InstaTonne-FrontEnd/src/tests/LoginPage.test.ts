import { mount } from "@vue/test-utils";
import { describe, expect, test } from "vitest";
import LoginPage from '../components/LoginPage.vue'
import { setTimeout } from "timers/promises";

describe('LoginPage tests', async () => {
    test("mounts", async () => {
        const wrapper = await mount(LoginPage)

        // initially, show the loading animation
        const initialLoadingAnimation = wrapper.find(".loadingIcon")
        expect(initialLoadingAnimation.exists()).toBe(true)

        // wait for get request
        await setTimeout(500).then(() => {
            const header = wrapper.find("h1")
            expect(header.text()).toBe("InstaTonne")
        })

        // check the loading animation is hidden
        const finalLoadingAnimation = wrapper.find(".loadingIcon")
        expect(finalLoadingAnimation.exists()).toBe(false)
    })
})