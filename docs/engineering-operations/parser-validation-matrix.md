# Parser Validation Matrix

This matrix defines the minimum behavior expected from CareerCraft's resume
parser. It is a test-planning reference, not a replacement for automated tests.

| Input | Expected result |
|---|---|
| Valid text-based PDF | Text is extracted, normalized, and returned. |
| Valid DOCX | Paragraph text is extracted and normalized. |
| Valid UTF-8 TXT | Text is decoded and normalized. |
| Empty supported file | Request is rejected with an actionable validation error. |
| Unsupported extension | Request is rejected before analysis. |
| Unsupported MIME type | Request is rejected even when the extension looks valid. |
| File above 5 MB | Request is rejected without parsing the full document. |
| Malformed PDF | Request fails safely without an internal traceback in the response. |
| Malformed DOCX | Request fails safely without partial or misleading output. |
| Image-only PDF | No fabricated text is returned; the limitation is made clear. |
| Text with ligatures | Common ligatures are normalized when supported. |
| Text with repeated whitespace | Whitespace is normalized without joining unrelated words. |
| Resume without standard headings | Extracted text is returned even when section coverage is low. |
| Duplicate section headings | Detection remains deterministic. |

## Security checks

- Treat uploaded bytes as untrusted input.
- Do not execute macros, embedded scripts, links, or document actions.
- Do not use the original filename as a server-side path.
- Do not include extracted resume text in exception messages or logs.
- Apply size validation before expensive parsing work.
- Keep parser behavior deterministic for identical input.

## Regression rule

Every parser bug fix should add the smallest fixture that reproduces the issue,
plus one assertion for the expected result and one assertion that sensitive
document content is not exposed through an error.
