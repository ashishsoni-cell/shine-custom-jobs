import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useParams } from 'react-router-dom';
import JobDescriptionPage from './components/JobDescriptionPage';

const sampleJob = {
  id: '123',
  title: 'Senior Product Manager',
  company: 'Shine Technologies',
  location: 'Bengaluru',
  experience: '5-8 yrs',
  salary: '₹20 - 28 LPA',
  employmentType: 'Full Time',
  isActive: true,
  isEarlyApplicant: true,
  skills: ['Product Strategy', 'Roadmap Planning', 'Stakeholder Management', 'Data Analysis'],
  description: `Lead the product team for India/SEA markets. Define roadmap, partner with engineering and design, and launch new user experiences that improve conversion and retention. Work closely with business, analytics, and marketing to prioritize features and drive measurable outcomes.`,
  companyDescription: 'A leading hiring platform that connects talent with growth-minded employers.',
  companyRating: 4.3,
  employees: '501–1,000',
  founded: 2018,
  companyLogoColor: '#1A56FF',
  companyInitial: 'ST',
};

const similarJobs = [
  {
    id: '456',
    title: 'Product Lead',
    company: 'Shine Ventures',
    location: 'Mumbai',
    experience: '4-7 yrs',
    salary: '₹18 - 24 LPA',
    employmentType: 'Full Time',
    skills: ['Go-to-market', 'Product Analytics', 'Customer Research'],
    description: 'Own product launches and cross-functional delivery for high-impact growth initiatives.',
    companyDescription: 'Fast-growing startup studio focused on consumer services.',
    companyRating: 4.1,
    employees: '201–500',
    founded: 2020,
    companyLogoColor: '#FF7A59',
    companyInitial: 'SV',
  },
  {
    id: '789',
    title: 'Principal Product Manager',
    company: 'Shine Labs',
    location: 'Hyderabad',
    experience: '7-10 yrs',
    salary: '₹24 - 32 LPA',
    employmentType: 'Full Time',
    skills: ['Leadership', 'Product Vision', 'Execution'],
    description: 'Drive product strategy across growth and engagement platforms.',
    companyDescription: 'Innovation lab for next-generation career products.',
    companyRating: 4.6,
    employees: '1,001–5,000',
    founded: 2015,
    companyLogoColor: '#38BDF8',
    companyInitial: 'SL',
  },
];

function JobTestRoute() {
  const { id } = useParams();
  return (
    <JobDescriptionPage
      job={{ ...sampleJob, id, title: `${sampleJob.title} (${id})` }}
      cohort="all-jobs"
      similarJobs={similarJobs}
      initialSaved={false}
    />
  );
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <main style={{
              minHeight: '100vh',
              padding: '48px 24px',
              fontFamily: 'var(--font-brand, system-ui, sans-serif)',
              background: '#090c14',
              color: '#fff',
            }}>
              <h1>Shine Job Description Route Test</h1>
              <p>Use the route below to render the job page in the browser.</p>
              <Link
                to="/job/123"
                style={{ color: '#7ea3ff', fontWeight: 700, textDecoration: 'none' }}>
                View sample job at /job/123
              </Link>
            </main>
          }
        />
        <Route path="/job/:id" element={<JobTestRoute />} />
      </Routes>
    </Router>
  );
}
