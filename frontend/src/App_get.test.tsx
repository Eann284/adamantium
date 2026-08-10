import {render, screen} from '@testing-library/react'
import App from "./App"


test('Get App', () => {
    render(<App/>)
    expect(screen.getByText(/Inventory Management/i)).toBeInTheDocument()
})