# fracture_classifier

```json
{
  "fractures": [
    {
      "id": "F1",
      "type": "doctrinal",
      "description": "Disagreement within the 6-justice majority over the controlling legal doctrine. A 3-justice plurality rests its conclusion on the major questions doctrine, while a 3-justice concurrence rejects that doctrine and relies exclusively on ordinary statutory interpretation.",
      "side_a": {
        "position": "The President's claimed authority to impose tariffs under IEEPA is a question of 'vast economic and political significance' that requires a clear statement from Congress, which is absent here. The major questions doctrine is the appropriate tool for this analysis.",
        "justices": [
          "Roberts",
          "Gorsuch",
          "Barrett"
        ],
        "source_blocks": [
          "24-1287_roberts_majority_0005"
        ],
        "page_range": "13-20"
      },
      "side_b": {
        "position": "The major questions doctrine is unnecessary because ordinary principles of statutory interpretation (text, context, and statutory scheme) are sufficient to conclude that IEEPA does not authorize tariffs.",
        "justices": [
          "Kagan",
          "Sotomayor",
          "Jackson"
        ],
        "source_blocks": [
          "24-1287_kagan_concurrence_in_part_0001"
        ],
        "page_range": "78-80"
      },
      "related_holdings": [
        "H1",
        "R2"
      ],
      "doctrines_at_issue": [
        "major_questions",
        "statutory_interpretation",
        "clear_statement rule"
      ],
      "severity": "fundamental",
      "notes": "This is the primary fracture within the majority. While both sides agree on the outcome (H1), they diverge on the proper legal test. This disagreement is significant for future cases involving broad delegations of authority, as the scope and application of the major questions doctrine remain contested. Justice Kagan explicitly states she does 'not join the part of that opinion invoking the so-called major-questions doctrine.' (24-1287_kagan_concurrence_in_part_0001, p. 78)."
    },
    {
      "id": "F2",
      "type": "scope",
      "description": "Fundamental disagreement between the majority and the principal dissent on whether the statutory power to 'regulate...importation' encompasses the power to impose tariffs.",
      "side_a": {
        "position": "The power to 'regulate' does not include the power to tax. Tariffs are a form of taxation, distinct in kind from the other powers listed in IEEPA (e.g., block, prohibit). Congress always delegates tariff power specifically and did not do so in IEEPA.",
        "justices": [
          "Roberts",
          "Sotomayor",
          "Kagan",
          "Gorsuch",
          "Barrett",
          "Jackson"
        ],
        "source_blocks": [
          "24-1287_roberts_majority_0006"
        ],
        "page_range": "20-22"
      },
      "side_b": {
        "position": "The broad power to 'regulate...importation' naturally includes traditional tools of trade regulation like tariffs, alongside quotas and embargoes. Historical usage and precedent confirm this understanding.",
        "justices": [
          "Kavanaugh",
          "Thomas",
          "Alito"
        ],
        "source_blocks": [
          "24-1287_kavanaugh_dissent_0001",
          "24-1287_kavanaugh_dissent_0004"
        ],
        "page_range": "109, 117-120"
      },
      "related_holdings": [
        "H1",
        "R1"
      ],
      "doctrines_at_issue": [
        "statutory_interpretation",
        "emergency_powers",
        "taxing_power"
      ],
      "severity": "fundamental",
      "notes": "This is the central disagreement of the case, directly addressing the core holding (H1) and the majority's main reasoning (R1). Justice Kavanaugh's dissent argues that interpreting IEEPA to allow embargoes but not the 'lesser power of tariffs' does not 'make much sense.' (24-1287_kavanaugh_dissent_0001, p. 111)."
    },
    {
      "id": "F3",
      "type": "factual",
      "description": "Disagreement on the historical precedent and context surrounding IEEPA's enactment in 1977, specifically the significance of President Nixon's 1971 tariffs under the precursor statute, TWEA.",
      "side_a": {
        "position": "A 'single, expressly limited opinion from a specialized intermediate appellate court' (upholding the Nixon tariffs) did not establish a 'well-settled' meaning of 'regulate...importation' that Congress would have understood itself to be adopting in IEEPA.",
        "justices": [
          "Roberts",
          "Sotomayor",
          "Kagan",
          "Gorsuch",
          "Barrett",
          "Jackson"
        ],
        "source_blocks": [
          "24-1287_roberts_majority_0006"
        ],
        "page_range": "23-24"
      },
      "side_b": {
        "position": "When IEEPA was enacted in 1977 'in the wake of the Nixon and Ford tariffs and the Algonquin decision, Congress and the public plainly would have understood that the power to “regulate . . . importation” included tariffs.'",
        "justices": [
          "Kavanaugh",
          "Thomas",
          "Alito"
        ],
        "source_blocks": [
          "24-1287_kavanaugh_dissent_0001"
        ],
        "page_range": "109-110"
      },
      "related_holdings": [
        "H1",
        "R1"
      ],
      "doctrines_at_issue": [
        "statutory_interpretation"
      ],
      "severity": "significant",
      "notes": "This fracture concerns the characterization of the factual and legal landscape at the time of IEEPA's enactment. The majority dismisses the precedent as not 'well-settled,' while the dissent views it as dispositive context that defines the statutory terms."
    },
    {
      "id": "F4",
      "type": "doctrinal",
      "description": "Disagreement on whether the major questions doctrine should have an exception for matters of foreign affairs.",
      "side_a": {
        "position": "There is no foreign affairs exception to the major questions doctrine. The power to impose tariffs during peacetime was given by the Framers to 'Congress alone,' and there is no reason to expect Congress to relinquish this core power through vague language, regardless of foreign policy implications.",
        "justices": [
          "Roberts",
          "Gorsuch",
          "Barrett"
        ],
        "source_blocks": [
          "24-1287_roberts_majority_0005"
        ],
        "page_range": "18-19"
      },
      "side_b": {
        "position": "The Court has never before applied the major questions doctrine in the foreign affairs context. In this domain, courts traditionally recognize Congress's intent to grant the President broad discretion and do not use the doctrine as 'a thumb on the scale against the President.'",
        "justices": [
          "Kavanaugh",
          "Thomas",
          "Alito"
        ],
        "source_blocks": [
          "24-1287_kavanaugh_dissent_0001"
        ],
        "page_range": "112"
      },
      "related_holdings": [
        "R2"
      ],
      "doctrines_at_issue": [
        "major_questions",
        "foreign_affairs_power",
        "separation_of_powers"
      ],
      "severity": "significant",
      "notes": "This is a key doctrinal dispute between the plurality and the dissent over the scope of the major questions doctrine. Justice Gorsuch's concurrence extensively discusses and rejects this proposed exception as well (24-1287_gorsuch_concurrence_0013, pp. 57-63)."
    },
    {
      "id": "F5",
      "type": "methodological",
      "description": "Disagreement over the propriety and weight of using legislative history (specifically, committee reports) to interpret IEEPA's meaning.",
      "side_a": {
        "position": "Legislative history, such as the House and Senate Reports accompanying TWEA and IEEPA, is 'among the best evidence of what Congress sought to accomplish' and plainly shows that the purpose of the 'regulate...importation' language was to grant power to freeze foreign assets, not impose tariffs.",
        "justices": [
          "Jackson"
        ],
        "source_blocks": [
          "24-1287_jackson_concurrence_in_part_0001"
        ],
        "page_range": "85-87"
      },
      "side_b": {
        "position": "Legislative history is not a reliable tool for determining statutory meaning. The dissent declines 'the help of legislative history,' focusing instead on the public meaning of the text at the time of enactment.",
        "justices": [
          "Kavanaugh",
          "Thomas",
          "Alito"
        ],
        "source_blocks": [
          "24-1287_jackson_concurrence_in_part_0001"
        ],
        "page_range": "88"
      },
      "related_holdings": [
        "H1",
        "R1"
      ],
      "doctrines_at_issue": [
        "statutory_interpretation"
      ],
      "severity": "minor",
      "notes": "This reflects a classic methodological split on statutory interpretation. Justice Jackson, concurring, explicitly criticizes the dissent for declining to use legislative history (24-1287_jackson_concurrence_in_part_0001, p. 88, citing 24-1287_kavanaugh_dissent_0005, p. 124, n.11). While the plurality and Kagan concurrence do not rely on it, they do not reject it as forcefully as the dissent."
    },
    {
      "id": "F6",
      "type": "doctrinal",
      "description": "Disagreement over whether a broad delegation of tariff authority would violate the nondelegation doctrine.",
      "side_a": {
        "position": "A broad delegation of a core legislative power like taxation without an intelligible principle would raise serious constitutional concerns under the nondelegation doctrine, which reinforces the need to read IEEPA narrowly.",
        "justices": [
          "Gorsuch"
        ],
        "source_blocks": [
          "24-1287_gorsuch_concurrence_0013"
        ],
        "page_range": "57-58"
      },
      "side_b": {
        "position": "The power to impose duties on imports is not a core legislative power subject to the nondelegation doctrine. Historically, it was viewed as a power over foreign commerce that Congress could, and did, delegate to the President.",
        "justices": [
          "Thomas"
        ],
        "source_blocks": [
          "24-1287_thomas_dissent_0001"
        ],
        "page_range": "90-91"
      },
      "related_holdings": [
        "H1"
      ],
      "doctrines_at_issue": [
        "nondelegation",
        "separation_of_powers",
        "taxing_power"
      ],
      "severity": "significant",
      "notes": "This is a deeper constitutional disagreement between Justice Gorsuch's concurrence and Justice Thomas's dissent. While the majority opinion avoids reaching the nondelegation issue, these two justices articulate fundamentally different views on whether Congress *could* have delegated this authority even if it had wanted to."
    }
  ],
  "fracture_summary": {
    "total": 6,
    "by_type": {
      "doctrinal": 3,
      "factual": 1,
      "methodological": 1,
      "scope": 1,
      "remedial": 0
    },
    "most_fractured_doctrine": "major_questions"
  }
}
```
