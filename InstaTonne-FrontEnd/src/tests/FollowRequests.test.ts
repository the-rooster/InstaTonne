import { mount } from "@vue/test-utils";
import { describe, expect, test, vi } from "vitest";
import FollowRequests from '../components/FollowRequests.vue'
import { setTimeout } from "timers/promises";
import AuthorCard from '../components/AuthorCard.vue'

describe('FollowRequests tests', async () => {
    test("mounts", async () => {
        const wrapper = await mount(FollowRequests)

        // initially, show the loading animation
        const initialLoadingAnimation = wrapper.find(".loadingIcon")
        expect(initialLoadingAnimation.exists()).toBe(true)

        // wait for get request
        await setTimeout(500).then(() => {
            const authorCard = wrapper.findComponent(AuthorCard)
            expect(authorCard.exists()).toBe(true)
        })

        // check the loading animation is hidden
        const finalLoadingAnimation = wrapper.find(".loadingIcon")
        expect(finalLoadingAnimation.exists()).toBe(false)
    })
})