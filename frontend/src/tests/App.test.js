import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { BrowserRouter as Router } from 'react-router-dom';
import App from '../App';

test('validates that app routes are present in html', () => {
  render(
    <Router>
      <App />
    </Router>
  );

  const createUserRoute = screen.getByText(/Create User/i);
  const authorizeUserRoute = screen.getByText(/Authorize User/i);

  expect(createUserRoute).toBeInTheDocument();
  expect(authorizeUserRoute).toBeInTheDocument();
});
