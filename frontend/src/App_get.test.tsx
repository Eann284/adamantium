import {render, screen} from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import App from "./App"


test('Get App', () => {
    render(<App/>)
    expect(screen.getByText(/Inventory Management/i)).toBeInTheDocument()
})

test('renders without crashing', () => {
  render(
    <MemoryRouter>
      <App />
    </MemoryRouter>
  )
})