import { mount } from '@vue/test-utils'
import LoginTest from '@/components/Login.test.vue'
import { nextTick } from 'vue'

describe('LoginTest.vue', () => {
  it('отображает ошибку при пустом логине и пароле', async () => {
    const wrapper = mount(LoginTest)
    await wrapper.find('[data-test="submit"]').trigger('submit') // <-- Важно! именно submit, не click
    await nextTick()
    const error = wrapper.find('[data-test="error"]')
    console.log('ERROR HTML:', wrapper.html())
    expect(error.exists()).toBe(true)
    expect(error.text()).toBe('Неверный логин или пароль')
  })

  it('обновляет поля ввода', async () => {
    const wrapper = mount(LoginTest)
    await wrapper.find('[data-test="username"]').setValue('admin')
    await wrapper.find('[data-test="password"]').setValue('secret')
    expect(wrapper.find('[data-test="username"]').element.value).toBe('admin')
    expect(wrapper.find('[data-test="password"]').element.value).toBe('secret')
  })
})
