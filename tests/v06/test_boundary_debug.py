from sparkbrain.evaluation.v06_boundary_probe import run_canonical_boundary_suite


def test_boundary_probe_diagnostic() -> None:
    suite = run_canonical_boundary_suite()
    assert False, {
        "assessment": suite.assessment.state_dict(),
        "sham": {
            "main_boundary": suite.sham.main_boundary_count,
            "control_boundary": suite.sham.control_boundary_count,
            "main_external": suite.sham.main_external_count,
            "control_external": suite.sham.control_external_count,
            "main_link_count": suite.sham.main_link_consistent_count,
            "control_link_count": suite.sham.control_link_consistent_count,
            "main_reliability": suite.sham.main_link_reliability,
            "control_reliability": suite.sham.control_link_reliability,
            "main_terminal": suite.sham.main_internal_terminal_count,
            "control_terminal": suite.sham.control_internal_terminal_count,
        },
        "targeted": {
            "main_boundary": suite.targeted_port_suppression.main_boundary_count,
            "main_external": suite.targeted_port_suppression.main_external_count,
            "main_terminal": suite.targeted_port_suppression.main_internal_terminal_count,
        },
        "matched_random": {
            "main_boundary": suite.matched_random_port_suppression.main_boundary_count,
            "main_external": suite.matched_random_port_suppression.main_external_count,
            "main_terminal": suite.matched_random_port_suppression.main_internal_terminal_count,
        },
        "internal_only": {
            "main_boundary": suite.internal_only.main_boundary_count,
            "control_boundary": suite.internal_only.control_boundary_count,
            "main_external": suite.internal_only.main_external_count,
            "control_external": suite.internal_only.control_external_count,
            "link_count": suite.assessment.internal_only_link_count,
        },
    }
