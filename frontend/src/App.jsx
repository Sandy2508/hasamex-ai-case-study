
import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import './App.css'

const sections = [
  'Interview Guide',
  'Cross-Interview Analysis',
  'Ask AI',
]

const guideQuestions = [
  'How would you describe current adoption of robotic surgery in your market?',
  'What are the main barriers to adoption?',
  'How important are hospital budgets and ROI in purchasing decisions?',
  'How important are surgeon training and clinical outcomes?',
  'What adoption trend do you expect over the next 3–5 years?',
  'What is the typical hospital decision-making timeline for purchasing a new robotic system?',
]

const experts = [
  'Dr. Jean Martin',
  'Anna Keller',
  'Dr. Emily Carter',
]

function App() {
  const [activeSection, setActiveSection] = useState('Interview Guide')

  // Ask AI state
  const [question, setQuestion] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // Interview Guide state
  const [selectedExpert, setSelectedExpert] = useState('Dr. Jean Martin')
  const [selectedGuideQuestion, setSelectedGuideQuestion] = useState(
    guideQuestions[0]
  )
  const [guideResult, setGuideResult] = useState(null)
  const [guideLoading, setGuideLoading] = useState(false)
  const [guideError, setGuideError] = useState('')

  // Cross-Interview Analysis state
  const [compareResult, setCompareResult] = useState(null)
  const [compareLoading, setCompareLoading] = useState(false)
  const [compareError, setCompareError] = useState('')

  async function handleAsk() {
    if (!question.trim()) {
      setError('Please enter a question.')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await fetch('http://127.0.0.1:8000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question.trim() }),
      })

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`)
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(
        'Could not connect to the backend. Make sure the FastAPI server is running.'
      )
    } finally {
      setLoading(false)
    }
  }

  async function handleGuideSubmit() {
    if (!selectedExpert || !selectedGuideQuestion) {
      setGuideError('Please select an expert and a guide question.')
      return
    }

    setGuideLoading(true)
    setGuideError('')
    setGuideResult(null)

    try {
      const response = await fetch('http://127.0.0.1:8000/guide', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: selectedGuideQuestion,
          expert: selectedExpert,
        }),
      })

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`)
      }

      const data = await response.json()
      setGuideResult(data)
    } catch (err) {
      setGuideError(
        'Could not process the guide question. Make sure the FastAPI server is running and try again.'
      )
    } finally {
      setGuideLoading(false)
    }
  }

  async function handleCompare() {
    setCompareLoading(true)
    setCompareError('')
    setCompareResult(null)

    try {
      const response = await fetch('http://127.0.0.1:8000/compare', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`)
      }

      const data = await response.json()
      setCompareResult(data)
    } catch (err) {
      setCompareError(
        'Could not load the cross-interview analysis. Make sure the FastAPI server is running and try again.'
      )
    } finally {
      setCompareLoading(false)
    }
  }

  function renderEvidence(evidence, emptyMessage) {
    if (!evidence || evidence.length === 0) {
      return <p>{emptyMessage}</p>
    }

    return evidence.map((item, index) => (
      <article
        className="evidence-card"
        key={`${item.expert}-${item.timestamp}-${index}`}
      >
        <div className="evidence-meta">
          <strong>{item.expert}</strong>
          <span>{item.market}</span>
          <span>{item.timestamp}</span>
        </div>

        <p>{item.text}</p>
      </article>
    ))
  }

  return (
    <div className="app">
      <header className="app-header">
        <div>
          <h1>Hasamex Research Assistant</h1>
          <p>European Robotic Surgery Market</p>
        </div>

        <span className="header-tag">Expert Interview Analysis</span>
      </header>

      <nav className="section-nav">
        {sections.map((section) => (
          <button
            key={section}
            className={
              activeSection === section
                ? 'nav-button active'
                : 'nav-button'
            }
            onClick={() => setActiveSection(section)}
          >
            {section}
          </button>
        ))}
      </nav>

      <main className="main-content">
        {/* Ask AI */}
        {activeSection === 'Ask AI' && (
          <section>
            <h2>Ask across all interviews</h2>

            <p className="section-description">
              Ask a question about the expert interviews. Answers are generated
              from retrieved transcript evidence.
            </p>

            <div className="question-box">
              <label htmlFor="question">Your question</label>

              <textarea
                id="question"
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                placeholder="Example: What are the main barriers to robotic surgery adoption?"
                rows={4}
              />

              <button
                className="primary-button"
                onClick={handleAsk}
                disabled={loading}
              >
                {loading ? 'Analyzing transcripts...' : 'Ask AI'}
              </button>
            </div>

            {error && <p className="error-message">{error}</p>}

            {result && (
              <div className="results">
                <section className="answer-card">
                  <h3>Answer</h3>

                  <div className="answer-text">
                    <ReactMarkdown>{result.answer}</ReactMarkdown>
                  </div>
                </section>

                <section className="evidence-section">
                  <h3>Supporting evidence</h3>

                  {renderEvidence(
                    result.evidence,
                    'No supporting evidence was retrieved.'
                  )}
                </section>
              </div>
            )}
          </section>
        )}

        {/* Interview Guide */}
        {activeSection === 'Interview Guide' && (
          <section>
            <h2>Interview Guide</h2>

            <p className="section-description">
              Select an expert and a question from the interview guide to view
              an evidence-based answer with supporting transcript statements
              and timestamps.
            </p>

            <div className="question-box">
              <label htmlFor="expert-select">Select expert</label>

              <select
                id="expert-select"
                value={selectedExpert}
                onChange={(event) => setSelectedExpert(event.target.value)}
              >
                {experts.map((expert) => (
                  <option key={expert} value={expert}>
                    {expert}
                  </option>
                ))}
              </select>

              <label htmlFor="guide-question-select">
                Select interview-guide question
              </label>

              <select
                id="guide-question-select"
                value={selectedGuideQuestion}
                onChange={(event) =>
                  setSelectedGuideQuestion(event.target.value)
                }
              >
                {guideQuestions.map((guideQuestion, index) => (
                  <option key={index} value={guideQuestion}>
                    {`Q${index + 1}. ${guideQuestion}`}
                  </option>
                ))}
              </select>

              <button
                className="primary-button"
                onClick={handleGuideSubmit}
                disabled={guideLoading}
              >
                {guideLoading ? 'Analyzing interview...' : 'Get Answer'}
              </button>
            </div>

            {guideError && (
              <p className="error-message">{guideError}</p>
            )}

            {guideResult && (
              <div className="results">
                <section className="answer-card">
                  <h3>Answer</h3>

                  <p>
                    <strong>Expert:</strong> {selectedExpert}
                  </p>

                  <p>
                    <strong>Question:</strong> {selectedGuideQuestion}
                  </p>

                  <div className="answer-text">
                    <ReactMarkdown>{guideResult.answer}</ReactMarkdown>
                  </div>
                </section>

                <section className="evidence-section">
                  <h3>Supporting evidence</h3>

                  {renderEvidence(
                    guideResult.evidence,
                    'No supporting evidence was retrieved.'
                  )}
                </section>
              </div>
            )}
          </section>
        )}

        {/* Cross-Interview Analysis */}
        {activeSection === 'Cross-Interview Analysis' && (
          <section>
            <h2>Cross-Interview Analysis</h2>

            <p className="section-description">
              Compare common themes and differences across the France, Germany,
              and United Kingdom interviews, with supporting transcript
              statements and timestamps.
            </p>

            <div className="question-box">
              <p>
                Generate an analysis of the three expert interviews.
              </p>

              <button
                className="primary-button"
                onClick={handleCompare}
                disabled={compareLoading}
              >
                {compareLoading
                  ? 'Comparing interviews...'
                  : 'Generate Comparison'}
              </button>
            </div>

            {compareError && (
              <p className="error-message">{compareError}</p>
            )}

            {compareResult && (
              <div className="results">
                <section className="answer-card">
                  <h3>Common Themes and Differences</h3>

                  <div className="answer-text">
                    <ReactMarkdown>{compareResult.answer}</ReactMarkdown>
                  </div>
                </section>

                <section className="evidence-section">
                  <h3>Evidence from the Interviews</h3>

                  {renderEvidence(
                    compareResult.evidence,
                    'No supporting evidence was retrieved.'
                  )}
                </section>
              </div>
            )}
          </section>
        )}
      </main>

      <footer className="app-footer">
        Hasamex AI Case Study · Evidence-based expert interview analysis
      </footer>
    </div>
  )
}

export default App
