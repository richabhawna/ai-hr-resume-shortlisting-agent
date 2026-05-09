from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def evaluate_communication(candidate):
    text_length = len(str(candidate))

    if text_length > 1200:
        return 10
    elif text_length > 800:
        return 8
    elif text_length > 500:
        return 6
    else:
        return 4


def semantic_skill_match(candidate_skills, required_skills):
    matched = []

    for req_skill in required_skills:
        req_embedding = model.encode(req_skill, convert_to_tensor=True)

        for cand_skill in candidate_skills:
            cand_embedding = model.encode(cand_skill, convert_to_tensor=True)

            similarity = util.cos_sim(req_embedding, cand_embedding)

            if similarity > 0.65:
                matched.append(req_skill)
                break

    return list(set(matched))


def calculate_candidate_score(candidate, job):
    breakdown = {}
    explanations = []

    candidate_skills = candidate["skills"]
    required_skills = job["required_skills"]

    matched_skills = semantic_skill_match(candidate_skills, required_skills)

    # Skills (30)
    if required_skills:
        skills_score = (len(matched_skills) / len(required_skills)) * 30
    else:
        skills_score = 0

    breakdown["skills_score"] = round(skills_score, 2)

    explanations.append(
        f"Matched {len(matched_skills)} out of {len(required_skills)} required skills."
    )

    # Experience (25)
    candidate_exp = candidate["experience_years"]
    required_exp = job["experience_required"]

    if candidate_exp >= required_exp:
        exp_score = 25
        explanations.append("Candidate meets required experience.")
    else:
        exp_score = (candidate_exp / max(required_exp, 1)) * 25
        explanations.append("Candidate has less experience than required.")

    breakdown["experience_score"] = round(exp_score, 2)

    # Education (15)
    candidate_edu = candidate["education"].lower()
    required_edu = job["education_required"].lower()

    if required_edu in candidate_edu:
        edu_score = 15
        explanations.append("Candidate meets education requirement.")
    else:
        edu_score = 5
        explanations.append("Education partially matches requirement.")

    breakdown["education_score"] = edu_score

    # Projects (20)
    num_projects = len(candidate["projects"])

    if num_projects >= 3:
        project_score = 20
        explanations.append("Strong project portfolio.")
    elif num_projects == 2:
        project_score = 15
        explanations.append("Good project experience.")
    elif num_projects == 1:
        project_score = 10
        explanations.append("Limited project experience.")
    else:
        project_score = 0
        explanations.append("No projects found.")

    breakdown["projects_score"] = project_score

    # Communication (10)
    communication_score = evaluate_communication(candidate)
    breakdown["communication_score"] = communication_score
    explanations.append("Communication score estimated from resume completeness and structure.")

    total = (
        skills_score
        + exp_score
        + edu_score
        + project_score
        + communication_score
    )

    breakdown["total_score"] = round(total, 2)

    if total >= 80:
        recommendation = "Strong Hire"
    elif total >= 60:
        recommendation = "Consider"
    else:
        recommendation = "Reject"

    breakdown["recommendation"] = recommendation
    breakdown["matched_skills"] = matched_skills
    breakdown["explanations"] = explanations

    return breakdown