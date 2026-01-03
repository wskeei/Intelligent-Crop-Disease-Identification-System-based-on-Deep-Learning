import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useSettingsStore = defineStore('settings', () => {
    // Load from local storage or default
    const savedSettings = localStorage.getItem('app-settings')
    const initialState = savedSettings ? JSON.parse(savedSettings) : {
        theme: 'light',
        language: 'zh-CN',
        animations: true,
        confidenceThreshold: 0.75,
        model: 'resnet50',
        tta: false,
        notifyComplete: true,
        notifyAlert: true,
        weeklyReport: false
    }

    const settings = ref(initialState)

    // Watch for changes and save to local storage + apply effect
    watch(settings, (newSettings) => {
        localStorage.setItem('app-settings', JSON.stringify(newSettings))
        applyTheme(newSettings.theme)
    }, { deep: true, immediate: true })

    function applyTheme(theme: string) {
        const html = document.documentElement
        if (theme === 'dark') {
            html.classList.add('dark')
        } else if (theme === 'light') {
            html.classList.remove('dark')
        } else if (theme === 'auto') {
            if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
                html.classList.add('dark')
            } else {
                html.classList.remove('dark')
            }
        }
    }

    return { settings }
})
