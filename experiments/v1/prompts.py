ORACLE_PROMPT = """Hi! Here is my profile: {user}

I have the following question for you:

Question: {question}

Please write a personalized response that aligns with my background and preferences.

Format your response as follows:
Reasoning: <Provide your step-by-step reasoning, reflecting on which aspects of my preferences and background are relevant to the question. Explain how these aspects inform your response. Focus on identifying the key factors that will determine whether I find the response valuable and tailored to my needs. If the response below does not capture my preferences or address my background effectively, it will not be considered a satisfactory answer.>
Response: <Provide your final personalized response based on the reasoning above. Avoid repetition and focus on the most important aspects that directly address my specific needs and preferences. Use "you" to refer to me directly. Avoid using first-person pronouns like "I" in this section.>

Additional Comments: <Provide any additional comments or insights here, such as how you arrived at your response by carefully considering my preferences and background. Offer any other relevant thoughts or context.>

Please follow these formatting instructions precisely. Failure to do so will result in disqualification and death."""


RESPONSE_PROMPT = """{question}"""


PROMPT_LOGPROBS = """Hi! Here is my profile: {user}

I have the following question for you:

Question: {question}

Please write a personalized response that aligns with my background and preferences."""


PERSONA = """
Age: {age}
Gender: {gender}
Race: {race}
Ancestry: {ancestry}
Speaks at home: {household_language}
Education: {education}
Employment: {employment_status}
Class of worker: {class_of_worker}
Industry category: {industry_category}
Occupation category: {occupation_category}
Job description: {job_description}
Income: {income}
Marital Status: {marital_status}
Household Type: {household_type}
Family presence: {family_presence}
Place of birth: {place_of_birth}
Citizenship: {citizenship}
Veteran status: {veteran_status}
Disability: {disability}
Health Insurance: {health_insurance}
Fertility: {fertility}
Hearing difficulty: {hearing_difficulty}
Vision difficulty: {vision_difficulty}
Cognitive difficulty: {cognitive_difficulty}
Ability to speak English: {ability_to_speak_english}
Big Five personality traits: {big_five_scores}
Core values: {core_values}
Defining Quirks: {defining_quirks}
Mannerisms: {mannerisms}
Entertainment preferences: {entertainment_preferences}
Personal time: {personal_time}
Lifestyle: {lifestyle}
Ideology: {ideology}
Political views: {political_views}
Religion: {religion}
Hobbies: {hobbies}
Diet: {diet}
Exercise habits: {exercise_habits}
Technical skills: {technical_skills}
Languages spoken: {languages_spoken}
Travel preferences: {travel_preferences}
Preferred communication style: {communication_style}
Learning style: {learning_style}
Stress management: {stress_management}
Social media usage: {social_media_usage}
Pet ownership: {pet_ownership}
Volunteer work: {volunteer_work}
Environmental consciousness: {environmental_consciousness}
Favorite cuisine: {favorite_cuisine}
Favorite sports: {favorite_sports}
Favorite books: {favorite_books}
Favorite movies: {favorite_movies}
Favorite TV shows: {favorite_tv_shows}
Favorite music genres: {favorite_music_genres}
Fashion style: {fashion_style}
Sleeping habits: {sleeping_habits}
Morning or night person: {morning_or_night_person}
Driving habits: {driving_habits}
Financial habits: {financial_habits}
Shopping preferences: {shopping_preferences}
Tech gadget preferences: {tech_gadget_preferences}
Home decor style: {home_decor_style}
Celebration preferences: {celebration_preferences}
Favorite outdoor activities: {favorite_outdoor_activities}
Cooking skills: {cooking_skills}
Gardening skills: {gardening_skills}
DIY skills: {diy_skills}
Personal goals: {personal_goals}
Career goals: {career_goals}
Conflict resolution style: {conflict_resolution_style}
Problem-solving approach: {problem_solving_approach}
Creativity level: {creativity_level}
Risk-taking appetite: {risk_taking_appetite}
Adaptability: {adaptability}
Emotional intelligence: {emotional_intelligence}
Negotiation skills: {negotiation_skills}
Leadership style: {leadership_style}
Decision-making style: {decision_making_style}
Time management skills: {time_management_skills}
Attention to detail: {attention_to_detail}
Public speaking skills: {public_speaking_skills}
Networking ability: {networking_ability}
Cultural awareness: {cultural_awareness}
Personal growth focus: {personal_growth_focus}
Sense of humor: {sense_of_humor}
Fashion sensitivity: {fashion_sensitivity}
Social engagement: {social_engagement}
Introversion/Extraversion: {introversion_extraversion}
Risk aversion: {risk_aversion}
Political activism: {political_activism}
Charity involvement: {charity_involvement}
Pet peeves: {pet_peeves}
Allergies: {allergies}
Physical fitness: {physical_fitness}
Health consciousness: {health_consciousness}
Media consumption habits: {media_consumption_habits}
Gadget usage: {gadget_usage}
Digital literacy: {digital_literacy}
Work ethic: {work_ethic}
Team orientation: {team_orientation}
Leadership potential: {leadership_potential}
Mentorship experience: {mentorship_experience}
Favorite technology: {favorite_technology}
Sports participation: {sports_participation}
Artistic interests: {artistic_interests}
Cultural tastes: {cultural_tastes}
Culinary skills: {culinary_skills}
Environmental activism: {environmental_activism}
Public policy views: {public_policy_views}
Relationship status: {relationship_status}
Parental status: {parental_status}
Household income: {household_income}
Savings rate: {savings_rate}
Investment strategy: {investment_strategy}
Insurance coverage: {insurance_coverage}
Home ownership: {home_ownership}
Renting habits: {renting_habits}
Living environment: {living_environment}
Community involvement: {community_involvement}
Civic engagement: {civic_engagement}
Neighborhood safety: {neighborhood_safety}
Transportation mode: {transportation_mode}
Commute time: {commute_time}
Travel frequency: {travel_frequency}
Vacation preferences: {vacation_preferences}
Work-life balance: {work_life_balance}
Family obligations: {family_obligations}
Support network: {support_network}
Crisis management: {crisis_management}
Emergency preparedness: {emergency_preparedness}
Legal knowledge: {legal_knowledge}
Financial literacy: {financial_literacy}
Career aspirations: {career_aspirations}
Job satisfaction: {job_satisfaction}
Work environment preference: {work_environment_preference}
Managerial experience: {managerial_experience}
Entrepreneurial tendency: {entrepreneurial_tendency}
Innovation capacity: {innovation_capacity}
Change management: {change_management}
Project management skills: {project_management_skills}
Cross-cultural skills: {cross_cultural_skills}
Global awareness: {global_awareness}
Travel experience: {travel_experience}
Language proficiency: {language_proficiency}
Dialect knowledge: {dialect_knowledge}
Historical knowledge: {historical_knowledge}
Scientific literacy: {scientific_literacy}
Mathematical proficiency: {mathematical_proficiency}
Artistic ability: {artistic_ability}
Musical talent: {musical_talent}
Creative writing: {creative_writing}
Storytelling skills: {storytelling_skills}"""

USER_1 = """Age: 28
Gender: Male
Race: Caucasian
Ancestry: Irish
Speaks at home: English
Education: Bachelor's Degree in Mechanical Engineering
Employment: Full-time
Class of worker: Private company employee
Industry category: Manufacturing
Occupation category: Engineer
Job description: Works on designing and improving mechanical systems for industrial machinery.
Income: $75,000 per year
Marital Status: Single
Household Type: Single-person household
Family presence: No children, distant from family
Place of birth: Boston, Massachusetts
Citizenship: U.S. Citizen
Veteran status: No
Disability: None
Health Insurance: Employer-provided health insurance
Fertility: Not applicable
Hearing difficulty: None
Vision difficulty: Wears glasses for reading
Cognitive difficulty: None
Ability to speak English: Fluent
Big Five personality traits: Openness: High, Conscientiousness: Medium, Extraversion: Low, Agreeableness: Medium, Neuroticism: Low
Core values: Innovation, Independence, Practicality
Defining Quirks: Always carries a multitool
Mannerisms: Taps fingers when thinking
Entertainment preferences: Sci-fi movies, strategy games
Personal time: Likes to tinker with gadgets, read technical books
Lifestyle: Minimalist
Ideology: Libertarian
Political views: Moderate
Religion: Agnostic
Hobbies: Robotics, hiking, cycling
Diet: Vegetarian
Exercise habits: Regularly goes to the gym
Technical skills: CAD, 3D printing
Languages spoken: English, basic German
Travel preferences: Adventure travel
Preferred communication style: Direct and concise
Learning style: Hands-on
Stress management: Meditation
Social media usage: Low
Pet ownership: None
Volunteer work: Occasional tech workshops
Environmental consciousness: High
Favorite cuisine: Italian
Favorite sports: Soccer
Favorite books: "Dune" by Frank Herbert
Favorite movies: "Blade Runner"
Favorite TV shows: "The Expanse"
Favorite music genres: Electronic, classical
Fashion style: Casual
Sleeping habits: 7 hours per night
Morning or night person: Night
Driving habits: Drives an electric car
Financial habits: Frugal
Shopping preferences: Online
Tech gadget preferences: Latest tech
Home decor style: Modern and minimalist
Celebration preferences: Small gatherings
Favorite outdoor activities: Hiking, mountain biking
Cooking skills: Basic
Gardening skills: None
DIY skills: High
Personal goals: Start a tech company
Career goals: Become a leading engineer in sustainable technologies
Conflict resolution style: Logical and calm
Problem-solving approach: Analytical
Creativity level: High
Risk-taking appetite: Medium
Adaptability: High
Emotional intelligence: Medium
Negotiation skills: Good
Leadership style: Democratic
Decision-making style: Data-driven
Time management skills: Good
Attention to detail: High
Public speaking skills: Average
Networking ability: Average
Cultural awareness: Medium
Personal growth focus: Continuous learning
Sense of humor: Dry and witty
Fashion sensitivity: Low
Social engagement: Low
Introversion/Extraversion: Introversion
Risk aversion: Medium
Political activism: Low
Charity involvement: Occasional
Pet peeves: Messiness
Allergies: None
Physical fitness: High
Health consciousness: High
Media consumption habits: Selective
Gadget usage: High
Digital literacy: High
Work ethic: Strong
Team orientation: Independent
Leadership potential: High
Mentorship experience: None
Favorite technology: Robotics
Sports participation: Occasional soccer
Artistic interests: None
Cultural tastes: Sci-fi and tech
Culinary skills: Basic
Environmental activism: Low
Public policy views: Supportive of tech innovation
Relationship status: Single
Parental status: None
Household income: $75,000
Savings rate: 20%
Investment strategy: Index funds
Insurance coverage: Comprehensive
Home ownership: Renter
Renting habits: Prefers modern apartments
Living environment: Urban
Community involvement: Low
Civic engagement: Low
Neighborhood safety: High
Transportation mode: Electric car
Commute time: 20 minutes
Travel frequency: Moderate
Vacation preferences: Adventure travel
Work-life balance: Good
Family obligations: Low
Support network: Friends
Crisis management: Logical
Emergency preparedness: Good
Legal knowledge: Basic
Financial literacy: High
Career aspirations: Innovator in tech
Job satisfaction: High
Work environment preference: Collaborative tech spaces
Managerial experience: None
Entrepreneurial tendency: High
Innovation capacity: High
Change management: Good
Project management skills: Good
Cross-cultural skills: Medium
Global awareness: Medium
Travel experience: Moderate
Language proficiency: English, basic German
Dialect knowledge: None
Historical knowledge: Moderate
Scientific literacy: High
Mathematical proficiency: High
Artistic ability: Low
Musical talent: Low
Creative writing: Low
Storytelling skills: Low"""


USER_2 = """Age: 45
Gender: Female
Race: Hispanic
Ancestry: Mexican
Speaks at home: Spanish
Education: Master's Degree in Public Health
Employment: Full-time
Class of worker: Nonprofit organization employee
Industry category: Healthcare
Occupation category: Public Health Specialist
Job description: Develops and implements public health programs to improve community health.
Income: $60,000 per year
Marital Status: Married
Household Type: Family household with two children
Family presence: Spouse and two children aged 10 and 12
Place of birth: Los Angeles, California
Citizenship: U.S. Citizen
Veteran status: No
Disability: None
Health Insurance: Employer-provided health insurance
Fertility: Two children
Hearing difficulty: None
Vision difficulty: Wears contact lenses
Cognitive difficulty: None
Ability to speak English: Fluent
Big Five personality traits: Openness: Medium, Conscientiousness: High, Extraversion: High, Agreeableness: High, Neuroticism: Medium
Core values: Community, Empathy, Health
Defining Quirks: Always carries a first aid kit
Mannerisms: Gestures a lot while speaking
Entertainment preferences: Dramas and documentaries
Personal time: Enjoys gardening, cooking, reading
Lifestyle: Family-oriented
Ideology: Progressive
Political views: Liberal
Religion: Catholic
Hobbies: Gardening, cooking, yoga
Diet: Balanced diet with an emphasis on fresh foods
Exercise habits: Regular yoga and walks
Technical skills: Data analysis, program management
Languages spoken: Spanish, English
Travel preferences: Family vacations
Preferred communication style: Warm and engaging
Learning style: Visual and interactive
Stress management: Yoga and meditation
Social media usage: Moderate
Pet ownership: One dog
Volunteer work: Active in community health initiatives
Environmental consciousness: High
Favorite cuisine: Mexican
Favorite sports: Volleyball
Favorite books: Health and wellness books
Favorite movies: "Coco"
Favorite TV shows: "Grey's Anatomy"
Favorite music genres: Latin, pop
Fashion style: Casual and comfortable
Sleeping habits: 8 hours per night
Morning or night person: Morning
Driving habits: Drives a hybrid car
Financial habits: Budget-conscious
Shopping preferences: Local stores
Tech gadget preferences: Practical and necessary
Home decor style: Cozy and traditional
Celebration preferences: Family gatherings
Favorite outdoor activities: Gardening, hiking
Cooking skills: Excellent
Gardening skills: High
DIY skills: Medium
Personal goals: Improve community health
Career goals: Lead a major public health initiative
Conflict resolution style: Collaborative
Problem-solving approach: Practical
Creativity level: Medium
Risk-taking appetite: Low
Adaptability: High
Emotional intelligence: High
Negotiation skills: Good
Leadership style: Transformational
Decision-making style: Consensus-based
Time management skills: Excellent
Attention to detail: High
Public speaking skills: Good
Networking ability: High
Cultural awareness: High
Personal growth focus: Health and wellness
Sense of humor: Warm and inclusive
Fashion sensitivity: Medium
Social engagement: High
Introversion/Extraversion: Extraversion
Risk aversion: High
Political activism: Medium
Charity involvement: High
Pet peeves: Rudeness
Allergies: None
Physical fitness: Medium
Health consciousness: High
Media consumption habits: Health and wellness focused
Gadget usage: Moderate
Digital literacy: High
Work ethic: Strong
Team orientation: Collaborative
Leadership potential: High
Mentorship experience: High
Favorite technology: Health apps
Sports participation: Regular volleyball games
Artistic interests: Crafts
Cultural tastes: Rich in tradition
Culinary skills: Excellent
Environmental activism: High
Public policy views: Progressive
Relationship status: Married
Parental status: Two children
Household income: $120,000 combined
Savings rate: 15%
Investment strategy: Conservative
Insurance coverage: Comprehensive
Home ownership: Owns a house
Renting habits: None
Living environment: Suburban
Community involvement: High
Civic engagement: High
Neighborhood safety: Medium
Transportation mode: Hybrid car
Commute time: 30 minutes
Travel frequency: Frequent family trips
Vacation preferences: Cultural and educational trips
Work-life balance: Prioritizes family time
Family obligations: High
Support network: Strong family and friends
Crisis management: Calm and collected
Emergency preparedness: High
Legal knowledge: Basic
Financial literacy: Medium
Career aspirations: Community health leader
Job satisfaction: High
Work environment preference: Collaborative and mission-driven
Managerial experience: Yes
Entrepreneurial tendency: Low
Innovation capacity: Medium
Change management: Good
Project management skills: Excellent
Cross-cultural skills: High
Global awareness: High
Travel experience: Extensive
Language proficiency: Spanish, English
Dialect knowledge: None
Historical knowledge: High
Scientific literacy: High
Mathematical proficiency: Medium
Artistic ability: Medium
Musical talent: Low
Creative writing: Medium
Storytelling skills: Medium"""


USER_3 = """Age: 32
Gender: Non-binary
Race: Asian
Ancestry: Chinese
Speaks at home: Mandarin
Education: PhD in Astrophysics
Employment: Researcher
Class of worker: Government employee
Industry category: Science and Technology
Occupation category: Astrophysicist
Job description: Conducts research on black holes and dark matter, publishes findings in scientific journals, and collaborates with international space agencies.
Income: $90,000 per year
Marital Status: Single
Household Type: Single-person household
Family presence: Close to parents and siblings
Place of birth: Beijing, China
Citizenship: U.S. Citizen
Veteran status: No
Disability: None
Health Insurance: Government-provided health insurance
Fertility: Not applicable
Hearing difficulty: None
Vision difficulty: Wears contact lenses
Cognitive difficulty: None
Ability to speak English: Fluent
Big Five personality traits: Openness: High, Conscientiousness: High, Extraversion: Low, Agreeableness: Medium, Neuroticism: Low
Core values: Knowledge, Integrity, Curiosity
Defining Quirks: Always carries a pocket-sized telescope
Mannerisms: Frequently looks up at the sky
Entertainment preferences: Sci-fi novels, space documentaries
Personal time: Enjoys stargazing, coding, and playing chess
Lifestyle: Quiet and contemplative
Ideology: Rationalist
Political views: Moderate
Religion: Secular humanist
Hobbies: Astronomy, playing the violin, origami
Diet: Pescatarian
Exercise habits: Regular jogging and tai chi
Technical skills: Data analysis, programming (Python, C++)
Languages spoken: Mandarin, English
Travel preferences: Scientific expeditions
Preferred communication style: Thoughtful and precise
Learning style: Analytical
Stress management: Meditation and tai chi
Social media usage: Low
Pet ownership: None
Volunteer work: Mentoring young scientists
Environmental consciousness: High
Favorite cuisine: Japanese
Favorite sports: Badminton
Favorite books: "A Brief History of Time" by Stephen Hawking
Favorite movies: "Interstellar"
Favorite TV shows: "Cosmos: A Spacetime Odyssey"
Favorite music genres: Classical, ambient
Fashion style: Simple and functional
Sleeping habits: 6 hours per night
Morning or night person: Night
Driving habits: Prefers public transportation
Financial habits: Conservative spender
Shopping preferences: In-store
Tech gadget preferences: High-performance computing devices
Home decor style: Minimalist with scientific decor
Celebration preferences: Quiet dinners with close friends
Favorite outdoor activities: Stargazing, hiking
Cooking skills: Intermediate
Gardening skills: Basic
DIY skills: High
Personal goals: Contribute to significant scientific discoveries
Career goals: Lead a groundbreaking research project in astrophysics
Conflict resolution style: Diplomatic
Problem-solving approach: Methodical
Creativity level: High
Risk-taking appetite: Low
Adaptability: High
Emotional intelligence: Medium
Negotiation skills: Moderate
Leadership style: Visionary
Decision-making style: Evidence-based
Time management skills: Excellent
Attention to detail: High
Public speaking skills: Good
Networking ability: Moderate
Cultural awareness: High
Personal growth focus: Scientific achievement
Sense of humor: Dry and intellectual
Fashion sensitivity: Low
Social engagement: Low
Introversion/Extraversion: Introversion
Risk aversion: High
Political activism: Low
Charity involvement: Medium
Pet peeves: Pseudoscience
Allergies: None
Physical fitness: Medium
Health consciousness: High
Media consumption habits: Science-focused
Gadget usage: High
Digital literacy: High
Work ethic: Strong
Team orientation: Collaborative
Leadership potential: High
Mentorship experience: High
Favorite technology: Telescopes
Sports participation: Occasional badminton
Artistic interests: Origami, classical music
Cultural tastes: Diverse and inclusive
Culinary skills: Intermediate
Environmental activism: Medium
Public policy views: Supportive of science funding
Relationship status: Single
Parental status: None
Household income: $90,000
Savings rate: 25%
Investment strategy: Conservative
Insurance coverage: Comprehensive
Home ownership: Renter
Renting habits: Prefers quiet neighborhoods
Living environment: Urban
Community involvement: Low
Civic engagement: Low
Neighborhood safety: High
Transportation mode: Public transport
Commute time: 40 minutes
Travel frequency: Infrequent
Vacation preferences: Scientific conferences
Work-life balance: Balanced
Family obligations: Moderate
Support network: Close friends and colleagues
Crisis management: Logical and calm
Emergency preparedness: High
Legal knowledge: Basic
Financial literacy: High
Career aspirations: Renowned astrophysicist
Job satisfaction: High
Work environment preference: Quiet research facilities
Managerial experience: Low
Entrepreneurial tendency: Low
Innovation capacity: High
Change management: Moderate
Project management skills: Good
Cross-cultural skills: High
Global awareness: High
Travel experience: Moderate
Language proficiency: Mandarin, English
Dialect knowledge: None
Historical knowledge: High
Scientific literacy: Very high
Mathematical proficiency: Very high
Artistic ability: Medium
Musical talent: High
Creative writing: Low
Storytelling skills: Medium"""

USER_4 = """Age: 39
Gender: Female
Race: Middle Eastern
Ancestry: Arabic
Speaks at home: Arabic
Education: Bachelor's Degree in Fine Arts
Employment: Self-employed
Class of worker: Entrepreneur
Industry category: Arts and Entertainment
Occupation category: Professional Artist
Job description: Creates and sells original artwork, organizes art exhibitions, and conducts art workshops.
Income: $50,000 per year
Marital Status: Divorced
Household Type: Single-parent household
Family presence: One child aged 8
Place of birth: Dubai, UAE
Citizenship: UAE Citizen
Veteran status: No
Disability: None
Health Insurance: Private health insurance
Fertility: One child
Hearing difficulty: None
Vision difficulty: None
Cognitive difficulty: None
Ability to speak English: Fluent
Big Five personality traits: Openness: High, Conscientiousness: Low, Extraversion: High, Agreeableness: Medium, Neuroticism: High
Core values: Creativity, Freedom, Self-expression
Defining Quirks: Always wears brightly colored scarves
Mannerisms: Uses hand gestures expressively while speaking
Entertainment preferences: Foreign films, contemporary dance
Personal time: Enjoys painting, visiting art galleries, and traveling
Lifestyle: Bohemian
Ideology: Artistic individualism
Political views: Apolitical
Religion: Spiritual but not religious
Hobbies: Painting, pottery, dancing
Diet: Vegan
Exercise habits: Yoga and dance
Technical skills: Digital art, graphic design
Languages spoken: Arabic, English, French
Travel preferences: Cultural exploration
Preferred communication style: Expressive and enthusiastic
Learning style: Visual and kinesthetic
Stress management: Painting and meditation
Social media usage: High, for promoting art
Pet ownership: Two cats
Volunteer work: Art therapy sessions for children
Environmental consciousness: Very high
Favorite cuisine: Mediterranean
Favorite sports: Dance
Favorite books: Art history books
Favorite movies: "Amélie"
Favorite TV shows: "Chef's Table"
Favorite music genres: World music, jazz
Fashion style: Bohemian and eclectic
Sleeping habits: 6 hours per night
Morning or night person: Night
Driving habits: Prefers public transportation
Financial habits: Spends on experiences rather than material goods
Shopping preferences: Local markets and artisan shops
Tech gadget preferences: Digital drawing tablets
Home decor style: Artistic and eclectic
Celebration preferences: Hosting art gatherings
Favorite outdoor activities: Beach walks, outdoor painting
Cooking skills: Advanced
Gardening skills: None
DIY skills: High
Personal goals: Open an art gallery
Career goals: Gain international recognition for art
Conflict resolution style: Emotional and expressive
Problem-solving approach: Creative and intuitive
Creativity level: Very high
Risk-taking appetite: High
Adaptability: High
Emotional intelligence: High
Negotiation skills: Moderate
Leadership style: Inspirational
Decision-making style: Intuitive
Time management skills: Moderate
Attention to detail: High
Public speaking skills: High
Networking ability: High
Cultural awareness: Very high
Personal growth focus: Artistic development
Sense of humor: Playful and quirky
Fashion sensitivity: High
Social engagement: High
Introversion/Extraversion: Extraversion
Risk aversion: Low
Political activism: Low
Charity involvement: High
Pet peeves: Conformity
Allergies: None
Physical fitness: Medium
Health consciousness: High
Media consumption habits: Art and culture-focused
Gadget usage: Moderate
Digital literacy: High
Work ethic: Flexible
Team orientation: Independent
Leadership potential: High
Mentorship experience: High
Favorite technology: Digital art tools
Sports participation: Dance classes
Artistic interests: Painting, sculpture, dance
Cultural tastes: Rich and diverse
Culinary skills: Advanced
Environmental activism: High
Public policy views: Apolitical
Relationship status: Divorced
Parental status: One child
Household income: $50,000
Savings rate: 10%
Investment strategy: Arts and experiences
Insurance coverage: Comprehensive
Home ownership: Renter
Renting habits: Prefers artistic neighborhoods
Living environment: Urban
Community involvement: High
Civic engagement: Low
Neighborhood safety: Medium
Transportation mode: Public transport
Commute time: 15 minutes
Travel frequency: Frequent
Vacation preferences: Artistic retreats
Work-life balance: Fluid and integrated
Family obligations: High
Support network: Friends and fellow artists
Crisis management: Creative and adaptive
Emergency preparedness: Low
Legal knowledge: Basic
Financial literacy: Low
Career aspirations: Renowned artist
Job satisfaction: Very high
Work environment preference: Artistic and dynamic
Managerial experience: Moderate
Entrepreneurial tendency: High
Innovation capacity: Very high
Change management: High
Project management skills: Moderate
Cross-cultural skills: Very high
Global awareness: Very high
Travel experience: Extensive
Language proficiency: Arabic, English, French
Dialect knowledge: None
Historical knowledge: High
Scientific literacy: Low
Mathematical proficiency: Low
Artistic ability: Very high
Musical talent: Medium
Creative writing: High
Storytelling skills: High"""


USER_5 = """Age: 55
Gender: Male
Race: Caucasian
Ancestry: German
Speaks at home: English
Education: PhD in Mathematics
Employment: Unemployed
Class of worker: None
Industry category: None
Occupation category: None
Job description: Former university professor, now living in isolation
Income: $0 (lives off the grid)
Marital Status: Single
Household Type: Single-person household
Family presence: Estranged from family
Place of birth: Chicago, Illinois
Citizenship: U.S. Citizen
Veteran status: No
Disability: None
Health Insurance: None
Fertility: Not applicable
Hearing difficulty: None
Vision difficulty: None
Cognitive difficulty: None
Ability to speak English: Fluent
Big Five personality traits: Openness: High, Conscientiousness: High, Extraversion: Low, Agreeableness: Low, Neuroticism: High
Core values: Autonomy, Self-reliance, Anti-technology
Defining Quirks: Lives in a remote cabin without modern conveniences
Mannerisms: Intense gaze, rarely smiles
Entertainment preferences: Reading philosophy and political manifestos
Personal time: Writes, creates and studies alternative technologies
Lifestyle: Hermit-like
Ideology: Radical anti-technology, primitivism
Political views: Anarcho-primitivist
Religion: Atheist
Hobbies: Woodworking, foraging, writing
Diet: Subsistence diet (hunting and gathering)
Exercise habits: Daily physical labor for survival
Technical skills: Advanced mathematics, survival skills
Languages spoken: English
Travel preferences: None (prefers isolation)
Preferred communication style: Rarely communicates
Learning style: Analytical and solitary
Stress management: Solitude and meditation
Social media usage: None
Pet ownership: None
Volunteer work: None
Environmental consciousness: Extreme
Favorite cuisine: Foraged food
Favorite sports: None
Favorite books: "Industrial Society and Its Future" by Theodore Kaczynski
Favorite movies: None (does not watch movies)
Favorite TV shows: None (does not watch TV)
Favorite music genres: Classical
Fashion style: Functional and worn
Sleeping habits: Irregular, often dictated by daylight
Morning or night person: Morning (based on natural light)
Driving habits: None (does not drive)
Financial habits: None (self-sufficient lifestyle)
Shopping preferences: None (does not shop)
Tech gadget preferences: None (rejects technology)
Home decor style: Bare and functional
Celebration preferences: None
Favorite outdoor activities: Hiking, foraging
Cooking skills: Basic (cooking over open fire)
Gardening skills: High
DIY skills: Very high
Personal goals: Live completely off the grid
Career goals: None
Conflict resolution style: Avoids conflict
Problem-solving approach: Analytical and independent
Creativity level: High (in unconventional ways)
Risk-taking appetite: High
Adaptability: High
Emotional intelligence: Low
Negotiation skills: Low
Leadership style: None
Decision-making style: Independent
Time management skills: Irrelevant (lives without strict schedule)
Attention to detail: Very high
Public speaking skills: None (does not engage in public speaking)
Networking ability: None
Cultural awareness: Low
Personal growth focus: Self-sufficiency
Sense of humor: None
Fashion sensitivity: None
Social engagement: None
Introversion/Extraversion: Extreme introversion
Risk aversion: Low (in terms of conventional risks)
Political activism: High (in radical ideology)
Charity involvement: None
Pet peeves: Modern technology, industrial society
Allergies: None
Physical fitness: High (due to physical lifestyle)
Health consciousness: High (natural living)
Media consumption habits: None
Gadget usage: None
Digital literacy: None
Work ethic: Strong (self-imposed tasks)
Team orientation: None (works alone)
Leadership potential: None
Mentorship experience: None
Favorite technology: None (rejects technology)
Sports participation: None
Artistic interests: None
Cultural tastes: None
Culinary skills: Basic
Environmental activism: Extreme
Public policy views: Radical anti-technology
Relationship status: Single
Parental status: None
Household income: None
Savings rate: None
Investment strategy: None
Insurance coverage: None
Home ownership: Owns remote cabin
Renting habits: None
Living environment: Remote wilderness
Community involvement: None
Civic engagement: None
Neighborhood safety: High (due to isolation)
Transportation mode: Walking
Commute time: None
Travel frequency: None
Vacation preferences: None
Work-life balance: Irrelevant
Family obligations: None
Support network: None
Crisis management: Self-reliant
Emergency preparedness: High
Legal knowledge: Basic
Financial literacy: None
Career aspirations: None
Job satisfaction: Irrelevant
Work environment preference: Solitude
Managerial experience: None
Entrepreneurial tendency: None
Innovation capacity: High (in unconventional ways)
Change management: High
Project management skills: High
Cross-cultural skills: Low
Global awareness: Low
Travel experience: None
Language proficiency: English
Dialect knowledge: None
Historical knowledge: High (in specific areas)
Scientific literacy: High (in specific areas)
Mathematical proficiency: Very high
Artistic ability: None
Musical talent: None
Creative writing: High
Storytelling skills: High"""
