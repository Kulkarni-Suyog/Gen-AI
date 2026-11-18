# GSTSaral: 10 Realistic User Questions

These questions are written in the way a shopkeeper or customer might ask about the GST rate-change records currently available in `day4/data/records.json`. Record IDs refer to the 13-record dataset used by the FastAPI service.

| Q.No. | User question | Matching record ID | Can the current data answer it? |
|---:|---|---:|---|
| Q1 | What is the new GST rate on UHT milk, and when did it become effective? | 1 | Yes |
| Q2 | Has the GST on pre-packaged and labelled paneer changed? | 2 | Yes |
| Q3 | What GST rate now applies to roti, chapati and paratha? | 3 | Yes |
| Q4 | What was the old GST rate on hair oil and what is the new rate? | 4 | Yes |
| Q5 | What is the revised GST rate for shampoo? | 5 | Yes |
| Q6 | Will the GST rate on shampoo or other personal-care products increase next year? | None | **No** |
| Q7 | What is the current recorded GST rate for toilet soap bars? | 6 | Yes |
| Q8 | What is the new GST rate on bicycles? | 9 | Yes |
| Q9 | Are exercise books now under the Nil GST rate? | 10 | Yes |
| Q10 | What is the revised GST rate for toothpaste? | 7 | Yes |

## Why Q6 is marked No

The current GSTSaral dataset contains announced rate changes and their effective date. It does not contain future government decisions or forecasts. Therefore, it cannot know whether a rate will increase next year. The API should not guess. A user should check future GST Council announcements and official notifications when they are published.

## Notes

- Record IDs are the `record_id` values assigned by the Day 4 API from the order of records in its JSON file. They are not government notification numbers.
- A question marked Yes means the dataset contains a relevant rate-change record. It does not mean the record covers every possible product variant, HSN code or tax condition.
- The records are a learning dataset based on selected announcements from the 56th GST Council meeting press release. Check official notifications before using a rate for an actual invoice or tax filing.

## Source used by the learning dataset

56th GST Council meeting press release, 3 September 2025: https://gstcouncil.gov.in/sites/default/files/2025-09/press_release_press_information_bureau.pdf
