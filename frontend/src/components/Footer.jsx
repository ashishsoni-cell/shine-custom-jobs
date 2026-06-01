import { useMemo, useState } from 'react';
import { Link } from 'react-router-dom';

const BG = '#0D0D0D';
const WHITE = '#FFFFFF';
const MUTED = 'rgba(255,255,255,0.72)';
const BORDER = 'rgba(255,255,255,0.10)';
const SURFACE = '#13161F';
const SURFACE_LIGHT = 'rgba(255,255,255,0.04)';
const ACCENT = '#EAB308';
const GREEN = '#22C55E';

const footerStyles = {
  wrapper: {
    background: BG,
    color: WHITE,
    padding: '56px 24px 24px',
  },
  inner: {
    maxWidth: 1180,
    margin: '0 auto',
  },
  context: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: 40,
    paddingBottom: 40,
  },
  block: {
    display: 'flex',
    flexDirection: 'column',
    gap: 18,
  },
  heading: {
    margin: 0,
    fontSize: 18,
    fontWeight: 700,
    letterSpacing: '-0.01em',
    color: WHITE,
  },
  tabs: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: 8,
  },
  tab: selected => ({
    height: 32,
    padding: '0 14px',
    borderRadius: 999,
    border: `1px solid ${selected ? WHITE : BORDER}`,
    background: selected ? WHITE : 'transparent',
    color: selected ? BG : MUTED,
    fontWeight: 600,
    cursor: 'pointer',
  }),
  list: {
    display: 'flex',
    flexDirection: 'column',
    gap: 10,
  },
  listLink: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '10px 0',
    textDecoration: 'none',
    color: MUTED,
    borderBottom: `1px solid ${BORDER}`,
    transition: 'color 140ms ease, padding 140ms ease',
    fontSize: 13,
  },
  viewAll: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: 6,
    marginTop: 10,
    color: ACCENT,
    textDecoration: 'none',
    fontWeight: 700,
    fontSize: 13,
  },
  sitemap: {
    display: 'grid',
    gridTemplateColumns: '1.4fr 1fr 1fr 1fr',
    gap: 40,
    padding: '40px 0 32px',
    borderTop: `1px solid ${BORDER}`,
  },
  brandBlock: {
    maxWidth: 320,
    display: 'flex',
    flexDirection: 'column',
    gap: 16,
  },
  brandCopy: {
    margin: 0,
    fontSize: 13,
    lineHeight: 1.55,
    color: MUTED,
  },
  socials: {
    display: 'flex',
    gap: 8,
    flexWrap: 'wrap',
  },
  socialPill: {
    minWidth: 32,
    height: 32,
    borderRadius: 999,
    background: 'rgba(255,255,255,0.06)',
    border: `1px solid ${BORDER}`,
    color: WHITE,
    display: 'grid',
    placeItems: 'center',
    textDecoration: 'none',
    fontSize: 12,
    fontWeight: 700,
  },
  linkColumn: {
    display: 'flex',
    flexDirection: 'column',
    gap: 14,
  },
  colTitle: {
    margin: 0,
    fontSize: 11,
    fontWeight: 700,
    letterSpacing: '0.08em',
    textTransform: 'uppercase',
    color: WHITE,
  },
  colList: {
    margin: 0,
    padding: 0,
    listStyle: 'none',
    display: 'flex',
    flexDirection: 'column',
    gap: 10,
  },
  colLink: {
    textDecoration: 'none',
    color: MUTED,
    fontSize: 13,
  },
  partners: {
    padding: '22px 0',
    borderTop: `1px solid ${BORDER}`,
    display: 'flex',
    flexWrap: 'wrap',
    gap: 12,
    alignItems: 'center',
  },
  partnersLabel: {
    fontSize: 11,
    fontWeight: 700,
    letterSpacing: '0.10em',
    textTransform: 'uppercase',
    color: MUTED,
  },
  partnerPill: {
    height: 28,
    padding: '0 12px',
    borderRadius: 12,
    background: 'rgba(255,255,255,0.06)',
    border: `1px solid ${BORDER}`,
    color: WHITE,
    fontSize: 12,
    fontWeight: 700,
    textDecoration: 'none',
  },
  bottom: {
    paddingTop: 18,
    borderTop: `1px solid ${BORDER}`,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: 20,
    flexWrap: 'wrap',
  },
  bottomText: {
    fontSize: 12,
    color: MUTED,
  },
  bottomLinks: {
    display: 'flex',
    gap: 20,
    flexWrap: 'wrap',
  },
  bottomLink: {
    textDecoration: 'none',
    color: MUTED,
    fontSize: 12,
  },
};

const cityGroups = [
  {
    key: 'delhi',
    label: 'Delhi NCR',
    links: ['Jobs in Delhi', 'Jobs in Gurgaon', 'Jobs in Noida', 'Jobs in Faridabad'],
  },
  {
    key: 'bengaluru',
    label: 'Bengaluru',
    links: ['Jobs in Bengaluru', 'Jobs in Whitefield', 'Jobs in Electronic City', 'Jobs in Marathahalli'],
  },
  {
    key: 'mumbai',
    label: 'Mumbai',
    links: ['Jobs in Mumbai', 'Jobs in Navi Mumbai', 'Jobs in Thane', 'Jobs in Pune'],
  },
  {
    key: 'chennai',
    label: 'Chennai',
    links: ['Jobs in Chennai', 'Jobs in OMR', 'Jobs in Velachery', 'Jobs in Coimbatore'],
  },
];

const categoryGroups = [
  {
    key: 'tech',
    label: 'Tech',
    links: ['AI jobs', 'Data analyst jobs', 'Cyber security jobs', 'Data science jobs'],
  },
  {
    key: 'bpo',
    label: 'BPO',
    links: ['Customer service jobs', 'Voice process jobs', 'Non-voice process jobs', 'Tele-caller jobs'],
  },
  {
    key: 'bfsi',
    label: 'BFSI',
    links: ['Banking jobs', 'Insurance jobs', 'Investment banking jobs', 'Risk management jobs'],
  },
  {
    key: 'sales',
    label: 'Sales',
    links: ['Field sales jobs', 'Enterprise sales jobs', 'Inside sales jobs', 'Business development jobs'],
  },
];

export default function Footer() {
  const [selectedCity, setSelectedCity] = useState('delhi');
  const [selectedCategory, setSelectedCategory] = useState('tech');

  const currentCity = useMemo(
    () => cityGroups.find(group => group.key === selectedCity) || cityGroups[0],
    [selectedCity]
  );
  const currentCategory = useMemo(
    () => categoryGroups.find(group => group.key === selectedCategory) || categoryGroups[0],
    [selectedCategory]
  );

  return (
    <footer style={footerStyles.wrapper}>
      <div style={footerStyles.inner}>
        <div style={footerStyles.context}>
          <div style={footerStyles.block}>
            <h3 style={footerStyles.heading}>Jobs in top cities</h3>
            <div style={footerStyles.tabs}>
              {cityGroups.map(city => (
                <button
                  key={city.key}
                  type="button"
                  style={footerStyles.tab(city.key === selectedCity)}
                  onClick={() => setSelectedCity(city.key)}
                >
                  {city.label}
                </button>
              ))}
            </div>
            <div style={footerStyles.list}>
              {currentCity.links.map(link => (
                <Link key={link} to="/" style={footerStyles.listLink}>
                  <span>{link}</span>
                  <span style={{ display: 'inline-flex', alignItems: 'center' }}>→</span>
                </Link>
              ))}
            </div>
          </div>
          <div style={footerStyles.block}>
            <h3 style={footerStyles.heading}>Browse jobs in</h3>
            <div style={{ ...footerStyles.tabs, background: SURFACE_LIGHT, borderRadius: 999, padding: 4 }}>
              {categoryGroups.map(category => (
                <button
                  key={category.key}
                  type="button"
                  style={footerStyles.tab(category.key === selectedCategory)}
                  onClick={() => setSelectedCategory(category.key)}
                >
                  {category.label}
                </button>
              ))}
            </div>
            <div style={footerStyles.list}>
              {currentCategory.links.map(link => (
                <Link key={link} to="/" style={footerStyles.listLink}>
                  <span>{link}</span>
                  <span style={{ display: 'inline-flex', alignItems: 'center' }}>→</span>
                </Link>
              ))}
              <Link to="/" style={footerStyles.viewAll}>
                <span>View all</span>
                <span>→</span>
              </Link>
            </div>
          </div>
        </div>
        <div style={footerStyles.sitemap}>
          <div style={footerStyles.brandBlock}>
            <div style={{ width: 56, height: 56, borderRadius: 14, background: GREEN, display: 'grid', placeItems: 'center' }}>
              <span style={{ color: BG, fontWeight: 800 }}>S</span>
            </div>
            <p style={footerStyles.brandCopy}>
              India's most trusted job platform. 8L+ live roles, 50K+ verified employers, free to apply.
            </p>
            <div style={footerStyles.socials}>
              {['in', 'Ig', 'f', 'YT', 'X'].map(label => (
                <a key={label} href="#" style={footerStyles.socialPill} aria-label={label}>
                  {label}
                </a>
              ))}
            </div>
          </div>
          {['Job Seekers', 'Company', 'Employers'].map((column, index) => (
            <div key={column} style={footerStyles.linkColumn}>
              <h5 style={footerStyles.colTitle}>{column}</h5>
              <ul style={footerStyles.colList}>
                {(index === 0
                  ? ['Search jobs', 'Trending jobs', 'Courses', 'Job assistance services', 'Create a job alert']
                  : index === 1
                  ? ['About us', 'Careers', 'Contact us', 'Fraud alert', "FAQ's"]
                  : ['Post a job', 'Register/Log In', 'Shine Recruiter']
                ).map(link => (
                  <li key={link}>
                    <Link to="/" style={footerStyles.colLink}>
                      {link}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div style={footerStyles.partners}>
          <span style={footerStyles.partnersLabel}>Our partner sites</span>
          {['Livemint', 'Patrika', 'OTTplay', 'Indicshemaroo', 'HT', 'Desimartini'].map(name => (
            <a key={name} href="#" style={footerStyles.partnerPill}>
              {name}
            </a>
          ))}
        </div>
        <div style={footerStyles.bottom}>
          <span style={footerStyles.bottomText}>© 2026 Shine.com · All rights reserved</span>
          <div style={footerStyles.bottomLinks}>
            {['T&C', 'Privacy', 'Cookies'].map(link => (
              <Link key={link} to="/" style={footerStyles.bottomLink}>
                {link}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}
