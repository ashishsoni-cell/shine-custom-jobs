import { useEffect, useMemo, useRef, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import Footer from './Footer';

const BG = '#0D0D0D';
const CARD = '#11161F';
const SURFACE = '#141820';
const BORDER = 'rgba(255,255,255,0.12)';
const TEXT = '#F7F8FA';
const MUTED = 'rgba(255,255,255,0.72)';
const MUTED_LIGHT = 'rgba(255,255,255,0.50)';
const GREEN = '#22C55E';
const YELLOW = '#EAB308';
const WHITE = '#FFFFFF';
const BLUE = '#1A56FF';
const SHADOW = '0 16px 56px rgba(0, 0, 0, 0.35)';

const styles = {
  page: {
    minHeight: '100vh',
    background: BG,
    color: TEXT,
    fontFamily: 'Plus Jakarta Sans, system-ui, sans-serif',
  },
  container: {
    maxWidth: 1180,
    margin: '0 auto',
    padding: '0 24px',
  },
  topStrip: {
    display: 'flex',
    flexWrap: 'wrap',
    alignItems: 'center',
    gap: 16,
    padding: '24px 0 12px',
  },
  backButton: {
    width: 40,
    height: 40,
    borderRadius: 999,
    border: `1px solid ${BORDER}`,
    background: SURFACE,
    color: TEXT,
    display: 'grid',
    placeItems: 'center',
    cursor: 'pointer',
    textDecoration: 'none',
  },
  breadcrumb: {
    display: 'flex',
    flexWrap: 'wrap',
    alignItems: 'center',
    gap: 8,
    fontSize: 13,
    color: MUTED,
    lineHeight: 1,
  },
  breadcrumbLink: {
    color: MUTED,
    textDecoration: 'none',
  },
  crumbCurrent: {
    color: TEXT,
    fontWeight: 700,
  },
  crumbSep: {
    opacity: 0.55,
  },
  postedBy: {
    marginLeft: 'auto',
    minWidth: 200,
    textAlign: 'right',
    display: 'flex',
    flexDirection: 'column',
    gap: 4,
    color: MUTED,
  },
  postedLabel: {
    fontSize: 11,
    fontWeight: 600,
    letterSpacing: '0.08em',
    textTransform: 'uppercase',
  },
  postedName: {
    fontSize: 15,
    fontWeight: 700,
    color: WHITE,
  },
  content: {
    display: 'grid',
    gridTemplateColumns: '1fr 340px',
    gap: 24,
    alignItems: 'start',
    padding: '8px 0 24px',
  },
  mainCard: {
    background: CARD,
    border: `1px solid ${BORDER}`,
    borderRadius: 24,
    padding: 28,
    boxShadow: SHADOW,
    display: 'flex',
    flexDirection: 'column',
    minHeight: 520,
  },
  chipRow: {
    display: 'inline-flex',
    flexWrap: 'wrap',
    gap: 8,
    marginBottom: 18,
  },
  chip: tone => ({
    display: 'inline-flex',
    alignItems: 'center',
    padding: '6px 12px',
    borderRadius: 999,
    fontSize: 12,
    fontWeight: 700,
    color: tone === 'accent' ? BG : WHITE,
    background: tone === 'accent' ? YELLOW : GREEN,
  }),
  title: {
    margin: 0,
    fontSize: 34,
    lineHeight: 1.1,
    fontWeight: 800,
  },
  metaRow: {
    display: 'grid',
    gridTemplateColumns: 'repeat(4, minmax(0,1fr))',
    gap: 16,
    padding: '24px 0',
    borderTop: `1px solid ${BORDER}`,
    borderBottom: `1px solid ${BORDER}`,
  },
  metaItem: {
    display: 'flex',
    flexDirection: 'column',
    gap: 6,
  },
  metaLabel: {
    fontSize: 11,
    fontWeight: 700,
    letterSpacing: '0.08em',
    textTransform: 'uppercase',
    color: MUTED_LIGHT,
  },
  metaValue: {
    fontSize: 15,
    fontWeight: 800,
    color: WHITE,
  },
  banner: {
    display: 'flex',
    flexWrap: 'wrap',
    alignItems: 'center',
    gap: 16,
    padding: 18,
    borderRadius: 18,
    background: 'rgba(34,197,94,0.12)',
    border: `1px solid rgba(34,197,94,0.18)`,
    marginBottom: 28,
  },
  bannerText: {
    flex: 1,
    minWidth: 0,
    fontSize: 14,
    lineHeight: 1.5,
    color: WHITE,
  },
  bannerEmphasis: {
    color: GREEN,
    fontWeight: 800,
  },
  bannerButton: {
    background: GREEN,
    color: BG,
    border: 'none',
    borderRadius: 14,
    padding: '12px 18px',
    fontWeight: 700,
    cursor: 'pointer',
  },
  ctaRow: {
    display: 'flex',
    flexWrap: 'wrap',
    alignItems: 'center',
    gap: 12,
    marginTop: 'auto',
  },
  applyButton: {
    background: GREEN,
    color: BG,
    border: 'none',
    borderRadius: 16,
    padding: '14px 28px',
    fontSize: 15,
    fontWeight: 800,
    cursor: 'pointer',
    boxShadow: '0 8px 22px rgba(34,197,94,0.16)',
  },
  iconButton: {
    width: 48,
    height: 48,
    display: 'grid',
    placeItems: 'center',
    borderRadius: 16,
    border: `1px solid ${BORDER}`,
    background: SURFACE,
    color: WHITE,
    cursor: 'pointer',
  },
  sidebar: isDesktop => ({
    position: isDesktop ? 'sticky' : 'static',
    top: isDesktop ? 88 : 'auto',
    alignSelf: isDesktop ? 'start' : 'auto',
  }),
  companyCard: {
    background: CARD,
    border: `1px solid ${BORDER}`,
    borderRadius: 24,
    padding: 24,
    display: 'flex',
    flexDirection: 'column',
    gap: 20,
  },
  companyHead: {
    display: 'flex',
    alignItems: 'center',
    gap: 16,
  },
  companyLogo: bg => ({
    minWidth: 56,
    minHeight: 56,
    borderRadius: 16,
    background: bg,
    display: 'grid',
    placeItems: 'center',
    color: WHITE,
    fontWeight: 800,
    fontSize: 20,
  }),
  companyName: {
    margin: 0,
    fontSize: 18,
    fontWeight: 800,
    color: WHITE,
  },
  companyMeta: {
    fontSize: 13,
    color: MUTED,
    lineHeight: 1.5,
  },
  companyDetails: {
    display: 'grid',
    gap: 14,
    paddingTop: 8,
    borderTop: `1px solid ${BORDER}`,
  },
  companyStat: {
    display: 'grid',
    gap: 4,
  },
  statLabel: {
    fontSize: 11,
    color: MUTED_LIGHT,
    textTransform: 'uppercase',
    letterSpacing: '0.08em',
    fontWeight: 700,
  },
  statValue: {
    fontSize: 14,
    color: WHITE,
    fontWeight: 700,
  },
  section: {
    background: CARD,
    border: `1px solid ${BORDER}`,
    borderRadius: 24,
    padding: 28,
    marginBottom: 18,
  },
  sectionHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: 12,
    marginBottom: 20,
  },
  sectionTitle: {
    margin: 0,
    paddingLeft: 12,
    fontSize: 20,
    fontWeight: 800,
    color: WHITE,
    position: 'relative',
  },
  sectionTitleAccent: {
    content: '""',
    position: 'absolute',
    left: 0,
    top: 4,
    width: 4,
    height: 'calc(100% - 8px)',
    background: YELLOW,
    borderRadius: 999,
  },
  sectionCount: {
    marginLeft: 'auto',
    fontSize: 13,
    color: MUTED,
    fontWeight: 600,
  },
  skills: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: 10,
  },
  skillBadge: {
    padding: '10px 14px',
    borderRadius: 999,
    border: `1px solid ${BORDER}`,
    color: WHITE,
    fontSize: 13,
    fontWeight: 700,
    background: 'rgba(255,255,255,0.04)',
  },
  descriptionWrapper: {
    position: 'relative',
  },
  descriptionBody: isCollapsed => ({
    maxHeight: isCollapsed ? 420 : 'none',
    overflow: 'hidden',
    transition: 'max-height 240ms ease',
  }),
  fadeLayer: {
    content: '""',
    position: 'absolute',
    left: 0,
    right: 0,
    bottom: 0,
    height: 140,
    background: 'linear-gradient(180deg, rgba(13,13,13,0) 0%, rgba(13,13,13,1) 90%)',
    pointerEvents: 'none',
  },
  descriptionText: {
    fontSize: 15,
    lineHeight: 1.8,
    color: MUTED,
  },
  readMore: {
    marginTop: 18,
    border: 'none',
    background: GREEN,
    color: BG,
    borderRadius: 16,
    padding: '12px 22px',
    fontSize: 14,
    fontWeight: 700,
    cursor: 'pointer',
  },
  similarSection: {
    padding: '0 0 32px',
  },
  similarTitle: {
    margin: '0 0 18px',
    fontSize: 18,
    fontWeight: 700,
  },
  similarList: {
    display: 'grid',
    gap: 16,
  },
  emptyState: {
    padding: 24,
    borderRadius: 20,
    background: SURFACE,
    color: MUTED,
    textAlign: 'center',
  },
  stickyBar: {
    position: 'fixed',
    left: 0,
    right: 0,
    bottom: 0,
    zIndex: 60,
    background: '#090A0F',
    borderTop: `1px solid ${BORDER}`,
    boxShadow: '0 -16px 45px rgba(0,0,0,0.4)',
    transition: 'transform 260ms ease, opacity 240ms ease',
    pointerEvents: 'none',
  },
  stickyInner: {
    maxWidth: 1180,
    margin: '0 auto',
    padding: '12px 24px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: 12,
  },
  stickyMeta: {
    display: 'flex',
    flexDirection: 'column',
    gap: 4,
    minWidth: 0,
  },
  stickyRole: {
    fontSize: 15,
    fontWeight: 800,
    color: WHITE,
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  stickySub: {
    fontSize: 13,
    color: MUTED,
  },
  stickyActions: {
    display: 'flex',
    alignItems: 'center',
    gap: 10,
  },
  stickyIcon: {
    width: 44,
    height: 44,
    borderRadius: 999,
    border: `1px solid ${BORDER}`,
    background: SURFACE,
    color: WHITE,
    display: 'grid',
    placeItems: 'center',
    cursor: 'pointer',
    pointerEvents: 'auto',
  },
  stickyApply: {
    height: 44,
    borderRadius: 16,
    border: 'none',
    background: GREEN,
    color: BG,
    fontWeight: 700,
    padding: '0 22px',
    cursor: 'pointer',
    pointerEvents: 'auto',
  },
  loader: {
    minHeight: '60vh',
    display: 'grid',
    placeItems: 'center',
    color: MUTED,
  },
};

const getCompanyInitials = company => {
  if (!company) return 'C';
  return company
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map(word => word[0].toUpperCase())
    .join('');
};

const stringToColor = text => {
  const colors = ['#1A56FF', '#22C55E', '#EAB308', '#7C3AED', '#0B3FCC', '#F97316'];
  let hash = 0;
  for (let i = 0; i < text.length; i += 1) {
    hash = (hash * 31 + text.charCodeAt(i)) | 0;
  }
  return colors[Math.abs(hash) % colors.length];
};

const normalizeDescription = text => {
  if (!text) return [];
  const blocks = text
    .trim()
    .split(/\n\n+/)
    .map(block => block.trim())
    .filter(Boolean);

  return blocks.map((block, index) => {
    if (/^#{1,6}\s+/.test(block)) {
      const level = block.match(/^#+/)[0].length;
      const content = block.replace(/^#{1,6}\s+/, '');
      const Tag = `h${Math.min(level + 2, 4)}`;
      return (
        <Tag key={index} style={{ color: WHITE, margin: '24px 0 10px', fontSize: 16, fontWeight: 800 }}>
          {content}
        </Tag>
      );
    }

    const listLines = block.split('\n').filter(line => line.trim().startsWith('- '));
    if (listLines.length === block.split('\n').length && listLines.length > 0) {
      return (
        <ul key={index} style={{ paddingLeft: 22, margin: '0 0 16px', color: MUTED, lineHeight: 1.8 }}>
          {listLines.map(line => (
            <li key={line} style={{ marginBottom: 10 }}>
              {line.replace(/^-\s+/, '')}
            </li>
          ))}
        </ul>
      );
    }

    return (
      <p key={index} style={{ margin: '0 0 16px', color: MUTED, lineHeight: 1.8 }}>
        {block.split('\n').map((line, lineIndex) => (
          <span key={lineIndex}>
            {line}
            {lineIndex < block.split('\n').length - 1 ? <br /> : null}
          </span>
        ))}
      </p>
    );
  });
};

const copyToClipboard = async text => {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    return navigator.clipboard.writeText(text);
  }
  const textarea = document.createElement('textarea');
  textarea.value = text;
  textarea.style.position = 'fixed';
  textarea.style.opacity = '0';
  document.body.appendChild(textarea);
  textarea.focus();
  textarea.select();
  document.execCommand('copy');
  document.body.removeChild(textarea);
};

const SimilarJobCard = ({ job }) => {
  const logoBg = job.logoColor || stringToColor(job.company || 'Job');
  const chipTone = job.isActive ? 'success' : job.isEarly ? 'accent' : 'muted';
  return (
    <article style={{ background: CARD, border: `1px solid ${BORDER}`, borderRadius: 22, padding: 24, display: 'grid', gap: 18 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 14, flexWrap: 'wrap' }}>
        <div style={{ minWidth: 44, minHeight: 44, borderRadius: 16, background: logoBg, color: WHITE, fontWeight: 800, display: 'grid', placeItems: 'center' }}>
          {job.logoInitial || getCompanyInitials(job.company)}
        </div>
        <div style={{ flex: 1, minWidth: 0, display: 'flex', flexWrap: 'wrap', gap: 10, alignItems: 'center' }}>
          <span style={{ fontWeight: 700, color: WHITE, minWidth: 0, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{job.company}</span>
          {job.postedAt ? <span style={{ color: MUTED, fontSize: 13 }}>{job.postedAt}</span> : null}
          <span style={{ marginLeft: 'auto', display: 'flex', gap: 6, flexWrap: 'wrap' }}>
            {chipTone === 'success' ? (
              <span style={{ background: 'rgba(34,197,94,0.14)', color: GREEN, padding: '4px 10px', borderRadius: 999, fontWeight: 700, fontSize: 12 }}>Actively Hiring</span>
            ) : chipTone === 'accent' ? (
              <span style={{ background: 'rgba(234,179,8,0.16)', color: YELLOW, padding: '4px 10px', borderRadius: 999, fontWeight: 700, fontSize: 12 }}>Be An Early Applicant</span>
            ) : null}
          </span>
        </div>
      </div>
      <h3 style={{ margin: 0, fontSize: 20, fontWeight: 800, color: WHITE }}>{job.title}</h3>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 16, color: MUTED, fontSize: 13 }}>
        {job.experience ? <span>{job.experience}</span> : null}
        {job.salary ? <span>{job.salary}</span> : null}
        {job.location ? <span>{job.location}</span> : null}
      </div>
      <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', gap: 14, borderTop: `1px solid ${BORDER}`, paddingTop: 18, alignItems: 'center' }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10, alignItems: 'center', minWidth: 0 }}>
          <span style={{ color: MUTED, fontSize: 13, fontWeight: 700 }}>Required:</span>
          <span style={{ display: 'flex', flexWrap: 'wrap', gap: 8, color: WHITE, fontWeight: 700 }}>
            {(job.skills || []).map(skill => (
              <span key={skill} style={{ whiteSpace: 'nowrap' }}>{skill}</span>
            ))}
          </span>
        </div>
        <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
          <button type="button" style={{ ...styles.iconButton, borderRadius: 14, width: 44, height: 44 }} aria-label="Share job">
            <span style={{ fontSize: 16 }}>↗</span>
          </button>
          <button type="button" style={{ ...styles.applyButton, padding: '12px 18px' }}>
            Apply
          </button>
        </div>
      </div>
    </article>
  );
};

export default function JobDescriptionPage({
  job,
  cohort = 'all-jobs',
  similarJobs = [],
  onSaveToggle,
  onResumeClick,
  initialSaved = false,
}) {
  const navigate = useNavigate();
  const location = useLocation();
  const [saved, setSaved] = useState(initialSaved);
  const [shareStatus, setShareStatus] = useState('');
  const [descriptionExpanded, setDescriptionExpanded] = useState(false);
  const [isSticky, setIsSticky] = useState(false);
  const [isDesktop, setIsDesktop] = useState(false);
  const applyButtonRef = useRef(null);

  const cohortState = location.state?.cohort || cohort;
  const backTarget = location.state?.from || `/${cohortState}`;
  const locationLabel = job?.location || 'All India';
  const jobRoute = `/${cohortState}`;

  useEffect(() => {
    const updateDesktop = () => setIsDesktop(window.innerWidth >= 768);
    updateDesktop();
    window.addEventListener('resize', updateDesktop);
    return () => window.removeEventListener('resize', updateDesktop);
  }, []);

  useEffect(() => {
    if (!applyButtonRef.current || typeof IntersectionObserver === 'undefined') return undefined;

    const observer = new IntersectionObserver(
      entries => {
        setIsSticky(!entries[0].isIntersecting);
      },
      { rootMargin: '0px 0px -8px 0px', threshold: 0 }
    );
    observer.observe(applyButtonRef.current);
    return () => observer.disconnect();
  }, [applyButtonRef]);

  const handleSaveToggle = () => {
    const nextSaved = !saved;
    setSaved(nextSaved);
    if (typeof onSaveToggle === 'function') {
      onSaveToggle(nextSaved);
    }
  };

  const handleShare = async () => {
    const shareText = job ? `${job.title} at ${job.company}` : 'Job details';
    const shareUrl = window.location.href;
    try {
      if (navigator.share) {
        await navigator.share({ title: shareText, text: shareText, url: shareUrl });
      } else {
        await copyToClipboard(shareUrl);
      }
      setShareStatus('Link copied');
    } catch (error) {
      setShareStatus('Unable to share');
    }
    window.setTimeout(() => setShareStatus(''), 2200);
  };

  const handleApply = () => {
    window.open('https://www.shine.com/pages/myshine/job-apply-flow?job-apply-flow=true', '_blank');
  };

  const handleResumeClick = () => {
    if (typeof onResumeClick === 'function') {
      onResumeClick();
      return;
    }
    navigate('/profile?section=resume');
  };

  const statusChips = useMemo(() => {
    if (!job) return [];
    const chips = [];
    if (job.isActive !== false) {
      chips.push({ label: 'Actively Hiring', tone: 'success' });
    }
    if (job.isEarlyApplicant) {
      chips.push({ label: 'Be An Early Applicant', tone: 'accent' });
    }
    return chips;
  }, [job]);

  if (!job) {
    return <div style={styles.loader}>Loading job details…</div>;
  }

  const companyLogoBg = job.companyLogoColor || stringToColor(job.company || 'Company');
  const companyInitials = job.companyInitial || getCompanyInitials(job.company);
  const skills = Array.isArray(job.skills) ? job.skills : job.skills ? String(job.skills).split(',').map(s => s.trim()).filter(Boolean) : [];

  return (
    <div style={styles.page}>
      <div style={styles.container}>
        <div style={styles.topStrip}>
          <button type="button" onClick={() => navigate(backTarget)} style={styles.backButton} aria-label="Back">
            ←
          </button>
          <nav aria-label="Breadcrumb" style={styles.breadcrumb}>
            <Link to="/" style={styles.breadcrumbLink}>Home</Link>
            <span style={styles.crumbSep}>›</span>
            <Link to={jobRoute} style={styles.breadcrumbLink}>Jobs in {locationLabel}</Link>
            <span style={styles.crumbSep}>›</span>
            <Link to={jobRoute} style={styles.breadcrumbLink}>{job.title} Jobs in {locationLabel}</Link>
            <span style={styles.crumbSep}>›</span>
            <span style={styles.crumbCurrent}>{job.title}</span>
          </nav>
          <div style={styles.postedBy}>
            <span style={styles.postedLabel}>Posted By</span>
            <span style={styles.postedName}>{job.company}</span>
          </div>
        </div>
        <div style={styles.content}>
          <main style={styles.mainCard}>
            <div style={styles.chipRow}>
              {statusChips.map(chip => (
                <span key={chip.label} style={styles.chip(chip.tone)}>{chip.label}</span>
              ))}
            </div>
            <h1 style={styles.title}>{job.title}</h1>
            <div style={styles.metaRow}>
              <div style={styles.metaItem}>
                <span style={styles.metaLabel}>Location</span>
                <span style={styles.metaValue}>{job.location || 'All India'}</span>
              </div>
              <div style={styles.metaItem}>
                <span style={styles.metaLabel}>Experience</span>
                <span style={styles.metaValue}>{job.experience || 'Not specified'}</span>
              </div>
              <div style={styles.metaItem}>
                <span style={styles.metaLabel}>Salary</span>
                <span style={styles.metaValue}>{job.salary || 'Not disclosed'}</span>
              </div>
              <div style={styles.metaItem}>
                <span style={styles.metaLabel}>Type</span>
                <span style={styles.metaValue}>{job.employmentType || 'Full Time'}</span>
              </div>
            </div>
            <section style={styles.banner}>
              <div style={styles.bannerText}>
                Know where you stand before you apply. See your{' '}
                <span style={styles.bannerEmphasis}>resume match, skills, and gaps</span>{' '}
                for this role.
              </div>
              <button type="button" style={styles.bannerButton} onClick={handleResumeClick}>
                Add résumé
              </button>
            </section>
            <div style={styles.ctaRow} ref={applyButtonRef}>
              <button type="button" style={styles.applyButton} onClick={handleApply}>
                Apply Now
              </button>
              <button type="button" style={styles.iconButton} onClick={handleSaveToggle} aria-pressed={saved}>
                {saved ? '★' : '☆'}
              </button>
              <button type="button" style={styles.iconButton} onClick={handleShare}>
                ↗
              </button>
              {shareStatus ? <span style={{ color: MUTED, fontSize: 13 }}>{shareStatus}</span> : null}
            </div>
            {skills.length > 0 && (
              <section style={{ ...styles.section, marginTop: 28 }}>
                <div style={styles.sectionHeader}>
                  <h2 style={styles.sectionTitle}>Skills For This Role</h2>
                  <span style={styles.sectionCount}>{skills.length} skills</span>
                </div>
                <div style={styles.skills}>
                  {skills.map(skill => (
                    <span key={skill} style={styles.skillBadge}>{skill}</span>
                  ))}
                </div>
              </section>
            )}
            <section style={{ ...styles.section, marginTop: 28 }}>
              <div style={styles.sectionHeader}>
                <h2 style={styles.sectionTitle}>Job Description</h2>
                <span style={styles.sectionCount}>{descriptionExpanded ? 'Full description' : '~50% shown'}</span>
              </div>
              <div style={styles.descriptionWrapper}>
                <div style={styles.descriptionBody(!descriptionExpanded)}>
                  {job.descriptionHtml ? (
                    <div
                      style={styles.descriptionText}
                      dangerouslySetInnerHTML={{ __html: job.descriptionHtml }}
                    />
                  ) : (
                    <div style={styles.descriptionText}>{normalizeDescription(job.description)}</div>
                  )}
                </div>
                {!descriptionExpanded && <div style={styles.fadeLayer} />}
              </div>
              <button
                type="button"
                style={styles.readMore}
                onClick={() => setDescriptionExpanded(open => !open)}
                aria-expanded={descriptionExpanded}
              >
                {descriptionExpanded ? 'Show less' : 'Read full description'}
              </button>
            </section>
          </main>
          <aside style={styles.sidebar(isDesktop)}>
            <div style={styles.companyCard}>
              <div style={styles.companyHead}>
                <div style={styles.companyLogo(companyLogoBg)}>{companyInitials}</div>
                <div>
                  <h2 style={styles.companyName}>{job.company}</h2>
                  <p style={styles.companyMeta}>{job.companyDescription || 'Trusted employer hiring through Shine.'}</p>
                </div>
              </div>
              <div style={styles.companyDetails}>
                {typeof job.companyRating === 'number' ? (
                  <div style={styles.companyStat}>
                    <span style={styles.statLabel}>Rating</span>
                    <span style={styles.statValue}>{job.companyRating.toFixed(1)} / 5</span>
                  </div>
                ) : null}
                <div style={styles.companyStat}>
                  <span style={styles.statLabel}>Employees</span>
                  <span style={styles.statValue}>{job.employees || '1,001–5,000'}</span>
                </div>
                {job.founded ? (
                  <div style={styles.companyStat}>
                    <span style={styles.statLabel}>Founded</span>
                    <span style={styles.statValue}>{job.founded}</span>
                  </div>
                ) : null}
              </div>
            </div>
          </aside>
        </div>
        <section style={styles.similarSection}>
          <h2 style={styles.similarTitle}>Similar Jobs</h2>
          {similarJobs.length === 0 ? (
            <div style={styles.emptyState}>No similar jobs are available right now.</div>
          ) : (
            <div style={styles.similarList}>
              {similarJobs.map(similarJob => (
                <SimilarJobCard key={similarJob.id || similarJob.title} job={similarJob} />
              ))}
            </div>
          )}
        </section>
      </div>
      <Footer />
      <div
        style={{
          ...styles.stickyBar,
          transform: isSticky ? 'translateY(0)' : 'translateY(100%)',
          opacity: isSticky ? 1 : 0,
        }}
        aria-hidden={!isSticky}
      >
        <div style={styles.stickyInner}>
          <div style={styles.stickyMeta}>
            <span style={styles.stickyRole}>{job.title}</span>
            <span style={styles.stickySub}>{job.company} · {locationLabel} · {job.experience || 'Not specified'}</span>
          </div>
          <div style={styles.stickyActions}>
            <button type="button" style={styles.stickyIcon} onClick={handleSaveToggle} aria-pressed={saved}>
              {saved ? '★' : '☆'}
            </button>
            <button type="button" style={styles.stickyIcon} onClick={handleShare}>
              ↗
            </button>
            <button type="button" style={styles.stickyApply} onClick={handleApply}>
              Apply Now
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
