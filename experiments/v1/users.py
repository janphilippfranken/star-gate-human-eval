import json

PERSONA = """Age: {age}
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


USER_0 = """Age: 29
Gender: Female
Race: African
Ancestry: Somali
Speaks at home: Somali
Education: Bachelor's Degree in Marine Biology
Employment: Full-time
Class of worker: NGO employee
Industry category: Environmental Conservation
Occupation category: Marine Biologist
Job description: Conducts research on marine ecosystems, works on conservation projects, and educates local communities about marine preservation.
Income: $35,000 per year
Marital Status: Single
Household Type: Extended family household
Family presence: Lives with parents and three younger siblings
Place of birth: Mogadishu, Somalia
Citizenship: Somali Citizen
Veteran status: No
Disability: None
Health Insurance: NGO-provided health insurance
Fertility: Not applicable
Hearing difficulty: None
Vision difficulty: None
Cognitive difficulty: None
Ability to speak English: Fluent
Big Five personality traits: Openness: High, Conscientiousness: High, Extraversion: Medium, Agreeableness: High, Neuroticism: Low
Core values: Conservation, Education, Community
Defining Quirks: Always carries a field notebook
Mannerisms: Speaks with passion about marine life
Entertainment preferences: Nature documentaries, scientific journals
Personal time: Enjoys snorkeling, reading, and volunteering at local schools
Lifestyle: Eco-friendly and community-oriented
Ideology: Environmentalism
Political views: Progressive
Religion: Islam
Hobbies: Snorkeling, bird watching, teaching
Diet: Pescatarian
Exercise habits: Regular swimming and beach cleanups
Technical skills: Data analysis, scuba diving
Languages spoken: Somali, English
Travel preferences: Prefers eco-tourism and scientific expeditions
Preferred communication style: Thoughtful and educational
Learning style: Visual and hands-on
Stress management: Meditation and ocean walks
Social media usage: Low
Pet ownership: None
Volunteer work: Organizes community beach cleanups and educational programs
Environmental consciousness: Very high
Favorite cuisine: Somali seafood dishes
Favorite sports: Swimming
Favorite books: Environmental science literature
Favorite movies: Nature documentaries
Favorite TV shows: Educational programs about nature
Favorite music genres: Traditional Somali music, ambient
Fashion style: Practical and eco-friendly
Sleeping habits: 7 hours per night
Morning or night person: Morning
Driving habits: Prefers public transportation and cycling
Financial habits: Frugal and eco-conscious
Shopping preferences: Local and sustainable products
Tech gadget preferences: Minimalist and energy-efficient
Home decor style: Simple and natural
Celebration preferences: Family and community gatherings
Favorite outdoor activities: Snorkeling, hiking, beach cleanups
Cooking skills: Good (focuses on traditional and sustainable meals)
Gardening skills: High
DIY skills: Medium
Personal goals: Promote marine conservation in Somalia
Career goals: Become a leading expert in marine biology and conservation
Conflict resolution style: Diplomatic and calm
Problem-solving approach: Analytical and community-focused
Creativity level: Medium (focused on scientific solutions)
Risk-taking appetite: Low
Adaptability: High
Emotional intelligence: High
Negotiation skills: High
Leadership style: Transformational
Decision-making style: Data-driven
Time management skills: Good
Attention to detail: High
Public speaking skills: Good
Networking ability: Medium
Cultural awareness: Very high
Personal growth focus: Scientific and environmental development
Sense of humor: Warm and gentle
Fashion sensitivity: Medium
Social engagement: High
Introversion/Extraversion: Balanced
Risk aversion: Medium
Political activism: High (focused on environmental issues)
Charity involvement: High
Pet peeves: Environmental neglect, wastefulness
Allergies: None
Physical fitness: Medium (due to active lifestyle)
Health consciousness: Very high
Media consumption habits: Low (focuses on scientific and environmental content)
Gadget usage: Low
Digital literacy: Medium
Work ethic: Very strong
Team orientation: Highly collaborative
Leadership potential: High
Mentorship experience: Medium
Favorite technology: Environmental monitoring devices
Sports participation: Regularly swims and participates in beach cleanups
Artistic interests: None
Cultural tastes: Deeply rooted in Somali traditions
Culinary skills: Good
Environmental activism: Very high
Public policy views: Supportive of environmental protection and education
Relationship status: Single
Parental status: None
Household income: $35,000
Savings rate: Medium
Investment strategy: Low-risk, socially responsible investments
Insurance coverage: Basic
Home ownership: None (lives with family)
Renting habits: None
Living environment: Urban
Community involvement: Very high
Civic engagement: High
Neighborhood safety: Medium
Transportation mode: Public transport and cycling
Commute time: 20 minutes
Travel frequency: Low (prefers local community work)
Vacation preferences: Eco-tourism
Work-life balance: Well-balanced
Family obligations: High
Support network: Strong family and community ties
Crisis management: Calm and resourceful
Emergency preparedness: Medium
Legal knowledge: Basic
Financial literacy: Medium
Career aspirations: Promote marine conservation and education globally
Job satisfaction: Very high
Work environment preference: Collaborative and community-focused
Managerial experience: Medium
Entrepreneurial tendency: Low
Innovation capacity: High (in scientific solutions)
Change management: High
Project management skills: High
Cross-cultural skills: Very high
Global awareness: Very high
Travel experience: Medium (focus on scientific expeditions)
Language proficiency: Somali, English
Dialect knowledge: None
Historical knowledge: Medium
Scientific literacy: Very high
Mathematical proficiency: High
Artistic ability: Low
Musical talent: Low
Creative writing: Medium
Storytelling skills: High"""


USER_1 = """Age: 45
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


USER_2 = """Age: 32
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


USER_3 = """Age: 39
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


USER_4 = """Age: 55
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


USER_5 = """Age: 22
Gender: Female
Race: African American
Ancestry: Nigerian
Speaks at home: Yoruba
Education: Associate's Degree in Graphic Design
Employment: Part-time
Class of worker: Freelance
Industry category: Media and Communication
Occupation category: Graphic Designer
Job description: Creates visual content for various digital platforms, specializing in social media graphics.
Income: $30,000 per year
Marital Status: Single
Household Type: Roommate household
Family presence: Close to parents and three siblings
Place of birth: Houston, Texas
Citizenship: U.S. Citizen
Veteran status: No
Disability: None
Health Insurance: None
Fertility: Not applicable
Hearing difficulty: None
Vision difficulty: None
Cognitive difficulty: None
Ability to speak English: Fluent
Big Five personality traits: Openness: High, Conscientiousness: Medium, Extraversion: High, Agreeableness: High, Neuroticism: Medium
Core values: Creativity, Diversity, Community
Defining Quirks: Always wears a different pair of colorful socks
Mannerisms: Often hums while working
Entertainment preferences: Animated films, puzzle games
Personal time: Enjoys sketching, playing video games
Lifestyle: Urban and social
Ideology: Egalitarian
Political views: Progressive
Religion: Christian
Hobbies: Digital art, reading comics, roller skating
Diet: Omnivorous with a preference for spicy foods
Exercise habits: Participates in local dance classes
Technical skills: Adobe Creative Suite, HTML/CSS
Languages spoken: English, Yoruba
Travel preferences: Group travel with friends
Preferred communication style: Visual and engaging
Learning style: Visual and experiential
Stress management: Drawing and listening to music
Social media usage: High (for networking and showcasing work)
Pet ownership: One hamster
Volunteer work: Mentors aspiring young artists
Environmental consciousness: Medium
Favorite cuisine: Nigerian
Favorite sports: Roller derby
Favorite books: Graphic novels
Favorite movies: "Spider-Man: Into the Spider-Verse"
Favorite TV shows: "Steven Universe"
Favorite music genres: Hip-hop, indie pop
Fashion style: Trendy and vibrant
Sleeping habits: 8 hours per night
Morning or night person: Night
Driving habits: Uses ride-sharing services
Financial habits: Budget-conscious
Shopping preferences: Thrift stores and online
Tech gadget preferences: High-performance tablets
Home decor style: Eclectic and colorful
Celebration preferences: Attends music festivals and art shows
Favorite outdoor activities: Roller skating, attending outdoor concerts
Cooking skills: Beginner
Gardening skills: None
DIY skills: Medium
Personal goals: Create a popular webcomic
Career goals: Become a renowned graphic designer in the entertainment industry
Conflict resolution style: Diplomatic and creative
Problem-solving approach: Innovative
Creativity level: Very high
Risk-taking appetite: Medium
Adaptability: High
Emotional intelligence: High
Negotiation skills: Moderate
Leadership style: Collaborative
Decision-making style: Creative
Time management skills: Average
Attention to detail: High
Public speaking skills: Average
Networking ability: High
Cultural awareness: High
Personal growth focus: Creative development
Sense of humor: Playful and witty
Fashion sensitivity: High
Social engagement: High
Introversion/Extraversion: Extraversion
Risk aversion: Medium
Political activism: Medium
Charity involvement: Medium
Pet peeves: Boredom
Allergies: None
Physical fitness: Medium
Health consciousness: Medium
Media consumption habits: High (focus on digital art and design)
Gadget usage: High
Digital literacy: High
Work ethic: Strong
Team orientation: Collaborative
Leadership potential: High
Mentorship experience: Medium
Favorite technology: Graphic tablets
Sports participation: Regularly participates in roller derby
Artistic interests: Digital art, animation
Cultural tastes: Contemporary and diverse
Culinary skills: Beginner
Environmental activism: Low
Public policy views: Supportive of arts and culture funding
Relationship status: Single
Parental status: None
Household income: $30,000
Savings rate: 10%
Investment strategy: Low-risk investments
Insurance coverage: Minimal
Home ownership: Renter
Renting habits: Prefers shared apartments
Living environment: Urban
Community involvement: Medium
Civic engagement: Medium
Neighborhood safety: Medium
Transportation mode: Ride-sharing
Commute time: 10 minutes
Travel frequency: Moderate
Vacation preferences: Attends conventions and festivals
Work-life balance: Balanced
Family obligations: Medium
Support network: Close friends and family
Crisis management: Creative and calm
Emergency preparedness: Basic
Legal knowledge: Low
Financial literacy: Medium
Career aspirations: Leading designer in entertainment
Job satisfaction: High
Work environment preference: Creative and dynamic
Managerial experience: Low
Entrepreneurial tendency: Medium
Innovation capacity: High
Change management: Good
Project management skills: Moderate
Cross-cultural skills: High
Global awareness: High
Travel experience: Moderate
Language proficiency: English, Yoruba
Dialect knowledge: None
Historical knowledge: Medium
Scientific literacy: Low
Mathematical proficiency: Low
Artistic ability: Very high
Musical talent: Low
Creative writing: Medium
Storytelling skills: High"""


USER_6 = """Age: 50
Gender: Male
Race: Caucasian
Ancestry: Scottish
Speaks at home: English
Education: High School Diploma
Employment: Full-time
Class of worker: Self-employed
Industry category: Agriculture
Occupation category: Farmer
Job description: Manages a family-owned farm, growing various crops and raising livestock.
Income: $45,000 per year
Marital Status: Married
Household Type: Family household with three children
Family presence: Spouse and three children aged 16, 14, and 10
Place of birth: Jackson, Mississippi
Citizenship: U.S. Citizen
Veteran status: No
Disability: None
Health Insurance: Private health insurance
Fertility: Three children
Hearing difficulty: None
Vision difficulty: None
Cognitive difficulty: None
Ability to speak English: Fluent
Big Five personality traits: Openness: Low, Conscientiousness: High, Extraversion: Medium, Agreeableness: High, Neuroticism: Low
Core values: Tradition, Hard work, Family
Defining Quirks: Always wears a cowboy hat
Mannerisms: Tends to speak slowly and thoughtfully
Entertainment preferences: Western movies, country music
Personal time: Enjoys fishing, woodworking
Lifestyle: Rural and community-focused
Ideology: Conservative
Political views: Traditional
Religion: Baptist
Hobbies: Fishing, hunting, woodworking
Diet: Omnivorous with a preference for home-cooked meals
Exercise habits: Daily farm work
Technical skills: Basic machinery repair, animal husbandry
Languages spoken: English
Travel preferences: Prefers local trips with family
Preferred communication style: Direct and straightforward
Learning style: Hands-on and practical
Stress management: Fishing and prayer
Social media usage: Low
Pet ownership: Two dogs and several farm animals
Volunteer work: Active in church activities
Environmental consciousness: Medium
Favorite cuisine: Southern comfort food
Favorite sports: College football
Favorite books: Western novels
Favorite movies: "The Good, the Bad and the Ugly"
Favorite TV shows: "Yellowstone"
Favorite music genres: Country, bluegrass
Fashion style: Practical and rugged
Sleeping habits: 7 hours per night
Morning or night person: Morning
Driving habits: Drives a pickup truck
Financial habits: Frugal and savings-focused
Shopping preferences: Local stores and farm supply shops
Tech gadget preferences: Basic and functional
Home decor style: Rustic and traditional
Celebration preferences: Family gatherings and barbecues
Favorite outdoor activities: Fishing, hunting
Cooking skills: Good (especially grilling)
Gardening skills: High
DIY skills: High
Personal goals: Expand the family farm
Career goals: Maintain a successful farm business
Conflict resolution style: Calm and practical
Problem-solving approach: Pragmatic
Creativity level: Low
Risk-taking appetite: Low
Adaptability: Medium
Emotional intelligence: High
Negotiation skills: Moderate
Leadership style: Authoritative
Decision-making style: Practical
Time management skills: Good
Attention to detail: High
Public speaking skills: Low
Networking ability: Medium
Cultural awareness: Low
Personal growth focus: Maintaining family and community traditions
Sense of humor: Dry and understated
Fashion sensitivity: Low
Social engagement: High
Introversion/Extraversion: Balanced
Risk aversion: High
Political activism: Low
Charity involvement: Medium
Pet peeves: Laziness
Allergies: None
Physical fitness: High (due to physical work)
Health consciousness: Medium
Media consumption habits: Low
Gadget usage: Low
Digital literacy: Low
Work ethic: Strong
Team orientation: Cooperative with family and local community
Leadership potential: High
Mentorship experience: Medium
Favorite technology: Farm equipment
Sports participation: Occasional hunting trips
Artistic interests: Woodworking
Cultural tastes: Traditional and local
Culinary skills: Good
Environmental activism: Low
Public policy views: Conservative
Relationship status: Married
Parental status: Three children
Household income: $45,000
Savings rate: 15%
Investment strategy: Low-risk investments
Insurance coverage: Comprehensive
Home ownership: Owns a house and farm
Renting habits: None
Living environment: Rural
Community involvement: High
Civic engagement: Medium
Neighborhood safety: High
Transportation mode: Pickup truck
Commute time: Minimal (works on the farm)
Travel frequency: Rarely travels far
Vacation preferences: Local family trips
Work-life balance: Integrated with family life
Family obligations: High
Support network: Strong family and community ties
Crisis management: Calm and resourceful
Emergency preparedness: High
Legal knowledge: Low
Financial literacy: Medium
Career aspirations: Maintain a thriving family farm
Job satisfaction: High
Work environment preference: Outdoors and hands-on
Managerial experience: High
Entrepreneurial tendency: Medium
Innovation capacity: Low
Change management: Medium
Project management skills: High
Cross-cultural skills: Low
Global awareness: Low
Travel experience: Low
Language proficiency: English
Dialect knowledge: Southern accent
Historical knowledge: Medium
Scientific literacy: Low
Mathematical proficiency: Low
Artistic ability: Medium (woodworking)
Musical talent: Low
Creative writing: Low
Storytelling skills: Medium"""


USER_7 = """Age: 35
Gender: Male
Race: Native American
Ancestry: Cherokee
Speaks at home: English
Education: Associate's Degree in Business Management
Employment: Full-time
Class of worker: Government employee
Industry category: Public Administration
Occupation category: Tribal Government Liaison
Job description: Facilitates communication and coordination between tribal government and federal agencies.
Income: $55,000 per year
Marital Status: Single
Household Type: Multi-generational household
Family presence: Lives with parents and a younger brother
Place of birth: Tulsa, Oklahoma
Citizenship: U.S. Citizen
Veteran status: No
Disability: None
Health Insurance: Government-provided health insurance
Fertility: Not applicable
Hearing difficulty: None
Vision difficulty: None
Cognitive difficulty: None
Ability to speak English: Fluent
Big Five personality traits: Openness: Medium, Conscientiousness: High, Extraversion: Medium, Agreeableness: High, Neuroticism: Medium
Core values: Community, Tradition, Respect
Defining Quirks: Always carries a small dreamcatcher keychain
Mannerisms: Often pauses to think before speaking
Entertainment preferences: Historical documentaries, indie films
Personal time: Enjoys beading, hiking, and learning about native plants
Lifestyle: Balanced between modern and traditional
Ideology: Community-oriented
Political views: Centrist
Religion: Traditional Native American spirituality
Hobbies: Beading, archery, traditional dancing
Diet: Omnivorous with a focus on locally-sourced food
Exercise habits: Regular hiking and archery practice
Technical skills: Project management, grant writing
Languages spoken: English, basic Cherokee
Travel preferences: Cultural and educational trips
Preferred communication style: Respectful and diplomatic
Learning style: Reflective and experiential
Stress management: Meditation and nature walks
Social media usage: Low
Pet ownership: One rescue dog
Volunteer work: Engaged in cultural preservation activities
Environmental consciousness: High
Favorite cuisine: Traditional Native American dishes
Favorite sports: Archery
Favorite books: Indigenous literature
Favorite movies: "Smoke Signals"
Favorite TV shows: "Reservation Dogs"
Favorite music genres: Folk, traditional drumming
Fashion style: Casual with cultural accents
Sleeping habits: 7 hours per night
Morning or night person: Morning
Driving habits: Drives a mid-size SUV
Financial habits: Conservative spender
Shopping preferences: Local artisans and farmers' markets
Tech gadget preferences: Basic and functional
Home decor style: Rustic with cultural elements
Celebration preferences: Participates in powwows and tribal events
Favorite outdoor activities: Hiking, foraging
Cooking skills: Intermediate
Gardening skills: High (focus on native plants)
DIY skills: Medium
Personal goals: Preserve and promote Cherokee culture
Career goals: Become a tribal leader
Conflict resolution style: Meditative and inclusive
Problem-solving approach: Holistic and community-focused
Creativity level: High (in cultural contexts)
Risk-taking appetite: Low
Adaptability: Medium
Emotional intelligence: High
Negotiation skills: High
Leadership style: Servant leadership
Decision-making style: Consensus-based
Time management skills: Good
Attention to detail: High
Public speaking skills: Good
Networking ability: High
Cultural awareness: Very high
Personal growth focus: Cultural and spiritual development
Sense of humor: Warm and inclusive
Fashion sensitivity: Medium
Social engagement: High
Introversion/Extraversion: Balanced
Risk aversion: Medium
Political activism: Medium
Charity involvement: High
Pet peeves: Disrespect towards nature
Allergies: None
Physical fitness: High (due to active lifestyle)
Health consciousness: High
Media consumption habits: Educational and cultural content
Gadget usage: Low
Digital literacy: Medium
Work ethic: Strong
Team orientation: Collaborative
Leadership potential: High
Mentorship experience: High
Favorite technology: Communication tools for community organization
Sports participation: Regular archery practice
Artistic interests: Beading, storytelling
Cultural tastes: Rich and diverse
Culinary skills: Intermediate
Environmental activism: High
Public policy views: Supportive of tribal sovereignty
Relationship status: Single
Parental status: None
Household income: $55,000
Savings rate: 20%
Investment strategy: Low-risk investments
Insurance coverage: Comprehensive
Home ownership: Family-owned house
Renting habits: None
Living environment: Suburban with access to natural areas
Community involvement: Very high
Civic engagement: High
Neighborhood safety: Medium
Transportation mode: SUV
Commute time: 30 minutes
Travel frequency: Frequent cultural trips
Vacation preferences: Cultural and educational trips
Work-life balance: Well-balanced
Family obligations: High
Support network: Strong family and community ties
Crisis management: Calm and resourceful
Emergency preparedness: High
Legal knowledge: Medium
Financial literacy: High
Career aspirations: Tribal leadership
Job satisfaction: High
Work environment preference: Collaborative and community-focused
Managerial experience: Moderate
Entrepreneurial tendency: Low
Innovation capacity: Medium
Change management: Good
Project management skills: High
Cross-cultural skills: Very high
Global awareness: Medium
Travel experience: Moderate
Language proficiency: English, basic Cherokee
Dialect knowledge: None
Historical knowledge: High
Scientific literacy: Medium
Mathematical proficiency: Low
Artistic ability: High
Musical talent: Medium
Creative writing: Medium
Storytelling skills: High"""


USER_8 = """Age: 58
Gender: Female
Race: Pacific Islander
Ancestry: Samoan
Speaks at home: English
Education: High School Diploma
Employment: Retired
Class of worker: Formerly self-employed
Industry category: Hospitality
Occupation category: Former Bed and Breakfast Owner
Job description: Ran a bed and breakfast, providing a welcoming stay for travelers, and organizing cultural tours.
Income: $35,000 per year (pension)
Marital Status: Widowed
Household Type: Single-person household
Family presence: Close to children and grandchildren
Place of birth: Pago Pago, American Samoa
Citizenship: U.S. Citizen
Veteran status: No
Disability: Mild arthritis
Health Insurance: Medicare
Fertility: Two children
Hearing difficulty: None
Vision difficulty: None
Cognitive difficulty: None
Ability to speak English: Fluent
Big Five personality traits: Openness: Medium, Conscientiousness: High, Extraversion: High, Agreeableness: High, Neuroticism: Low
Core values: Community, Tradition, Hospitality
Defining Quirks: Always wears a flower in her hair
Mannerisms: Warmly greets everyone with a smile
Entertainment preferences: Romantic comedies, traditional Samoan music
Personal time: Enjoys gardening, cooking traditional dishes, and spending time with family
Lifestyle: Community-oriented and relaxed
Ideology: Community-focused
Political views: Moderate
Religion: Christian (Methodist)
Hobbies: Gardening, knitting, storytelling
Diet: Omnivorous with a preference for fresh, local foods
Exercise habits: Regular walks and light gardening
Technical skills: Basic computer skills
Languages spoken: English, basic Samoan
Travel preferences: Prefers visiting family and friends
Preferred communication style: Warm and engaging
Learning style: Visual and hands-on
Stress management: Prayer and spending time in nature
Social media usage: Low
Pet ownership: One cat
Volunteer work: Active in church and community events
Environmental consciousness: High
Favorite cuisine: Samoan
Favorite sports: None
Favorite books: Inspirational and religious books
Favorite movies: "The Notebook"
Favorite TV shows: "Call the Midwife"
Favorite music genres: Traditional Samoan, gospel
Fashion style: Comfortable and traditional
Sleeping habits: 8 hours per night
Morning or night person: Morning
Driving habits: Drives occasionally
Financial habits: Frugal and budget-conscious
Shopping preferences: Local markets and small businesses
Tech gadget preferences: Basic and functional
Home decor style: Cozy and traditional
Celebration preferences: Family gatherings and community events
Favorite outdoor activities: Gardening, beach walks
Cooking skills: Excellent (specializes in traditional Samoan cuisine)
Gardening skills: High
DIY skills: Medium
Personal goals: Maintain a happy and healthy life
Career goals: None (already retired)
Conflict resolution style: Calm and diplomatic
Problem-solving approach: Practical and community-focused
Creativity level: Medium
Risk-taking appetite: Low
Adaptability: High
Emotional intelligence: High
Negotiation skills: Good
Leadership style: Nurturing and inclusive
Decision-making style: Collaborative
Time management skills: Good
Attention to detail: High
Public speaking skills: Good
Networking ability: High
Cultural awareness: Very high
Personal growth focus: Spiritual and community development
Sense of humor: Warm and gentle
Fashion sensitivity: Medium
Social engagement: High
Introversion/Extraversion: Extraversion
Risk aversion: High
Political activism: Low
Charity involvement: High
Pet peeves: Rudeness and dishonesty
Allergies: None
Physical fitness: Medium
Health consciousness: High
Media consumption habits: Low
Gadget usage: Low
Digital literacy: Basic
Work ethic: Strong
Team orientation: Collaborative
Leadership potential: Medium
Mentorship experience: High
Favorite technology: Simple and functional gadgets
Sports participation: None
Artistic interests: Knitting, traditional crafts
Cultural tastes: Traditional and community-oriented
Culinary skills: Excellent
Environmental activism: High
Public policy views: Supportive of community and family values
Relationship status: Widowed
Parental status: Two children
Household income: $35,000
Savings rate: Medium
Investment strategy: Conservative
Insurance coverage: Comprehensive
Home ownership: Owns a house
Renting habits: None
Living environment: Suburban
Community involvement: Very high
Civic engagement: Medium
Neighborhood safety: High
Transportation mode: Owns a car, prefers walking
Commute time: Minimal
Travel frequency: Low
Vacation preferences: Visits to family and friends
Work-life balance: Well-balanced
Family obligations: High
Support network: Strong family and community ties
Crisis management: Calm and resourceful
Emergency preparedness: Medium
Legal knowledge: Low
Financial literacy: Medium
Career aspirations: None (retired)
Job satisfaction: High
Work environment preference: Collaborative and community-focused
Managerial experience: High
Entrepreneurial tendency: Medium
Innovation capacity: Medium
Change management: Medium
Project management skills: Medium
Cross-cultural skills: Very high
Global awareness: Medium
Travel experience: Low
Language proficiency: English, basic Samoan
Dialect knowledge: None
Historical knowledge: Medium
Scientific literacy: Low
Mathematical proficiency: Low
Artistic ability: Medium
Musical talent: Low
Creative writing: Low
Storytelling skills: High"""

# elon (for debugging)
USER_9 = """Age: 52
Gender: Male
Race: Caucasian
Ancestry: South African
Speaks at home: English
Education: Bachelor's Degrees in Physics and Economics
Employment: Full-time
Class of worker: Entrepreneur
Industry category: Technology and Automotive
Occupation category: CEO
Job description: Leads multiple innovative companies focusing on space exploration, electric vehicles, and renewable energy.
Income: $300,000,000 per year
Marital Status: Divorced
Household Type: Single-person household
Family presence: Five children from previous marriages
Place of birth: Pretoria, South Africa
Citizenship: U.S. Citizen
Veteran status: No
Disability: None
Health Insurance: Private health insurance
Fertility: Five children
Hearing difficulty: None
Vision difficulty: None
Cognitive difficulty: None
Ability to speak English: Fluent
Big Five personality traits: Openness: Very High, Conscientiousness: High, Extraversion: High, Agreeableness: Low, Neuroticism: Medium
Core values: Innovation, Ambition, Sustainability
Defining Quirks: Frequently tweets controversial opinions
Mannerisms: Speaks rapidly and passionately about ideas
Entertainment preferences: Science fiction, technology blogs
Personal time: Enjoys reading, gaming, and experimenting with new tech
Lifestyle: High-paced and futuristic
Ideology: Technocrat
Political views: Libertarian
Religion: Atheist
Hobbies: Rocketry, AI development, video games
Diet: Omnivorous with a preference for simple meals
Exercise habits: Occasional workouts, prefers mentally stimulating activities
Technical skills: Programming, engineering, AI development
Languages spoken: English, basic Afrikaans
Travel preferences: Space travel, high-tech destinations
Preferred communication style: Direct and visionary
Learning style: Self-directed and hands-on
Stress management: Problem-solving and innovation
Social media usage: Very high
Pet ownership: None
Volunteer work: Supports science and technology education
Environmental consciousness: High
Favorite cuisine: Sushi
Favorite sports: None (focuses on tech and innovation)
Favorite books: "The Hitchhiker's Guide to the Galaxy" by Douglas Adams
Favorite movies: "Iron Man"
Favorite TV shows: "Rick and Morty"
Favorite music genres: Electronic, classical
Fashion style: Casual and functional
Sleeping habits: 6 hours per night
Morning or night person: Night
Driving habits: Drives an electric car (Tesla)
Financial habits: Invests heavily in tech ventures
Shopping preferences: Online
Tech gadget preferences: Cutting-edge and experimental tech
Home decor style: Modern and minimalist
Celebration preferences: Private celebrations with close friends
Favorite outdoor activities: Hiking, space exploration
Cooking skills: Basic
Gardening skills: None
DIY skills: High
Personal goals: Colonize Mars
Career goals: Revolutionize multiple industries
Conflict resolution style: Direct and uncompromising
Problem-solving approach: Innovative and data-driven
Creativity level: Very high
Risk-taking appetite: Very high
Adaptability: Very high
Emotional intelligence: Medium
Negotiation skills: High
Leadership style: Visionary and demanding
Decision-making style: Data-driven and instinctive
Time management skills: Excellent
Attention to detail: Very high
Public speaking skills: Good
Networking ability: High
Cultural awareness: Medium
Personal growth focus: Continuous learning and innovation
Sense of humor: Quirky and irreverent
Fashion sensitivity: Low
Social engagement: High
Introversion/Extraversion: Extraversion
Risk aversion: Very low
Political activism: Medium
Charity involvement: High (focus on tech and education)
Pet peeves: Inefficiency, bureaucracy
Allergies: None
Physical fitness: Medium
Health consciousness: Medium
Media consumption habits: High (focus on tech and innovation)
Gadget usage: Very high
Digital literacy: Very high
Work ethic: Extreme
Team orientation: Independent but collaborative when needed
Leadership potential: Very high
Mentorship experience: High
Favorite technology: SpaceX rockets, Tesla vehicles
Sports participation: None
Artistic interests: Sci-fi concepts
Cultural tastes: Futuristic and innovative
Culinary skills: Basic
Environmental activism: High (focus on renewable energy)
Public policy views: Supportive of tech innovation and deregulation
Relationship status: Divorced
Parental status: Five children
Household income: $300,000,000
Savings rate: Invests most earnings into ventures
Investment strategy: High-risk, high-reward
Insurance coverage: Comprehensive
Home ownership: Multiple properties
Renting habits: None
Living environment: Urban and high-tech
Community involvement: High (focus on tech communities)
Civic engagement: Medium
Neighborhood safety: High
Transportation mode: Electric car, private jet
Commute time: Minimal (often works remotely)
Travel frequency: Very high
Vacation preferences: Tech conferences, space-related trips
Work-life balance: Skewed towards work
Family obligations: Medium
Support network: High (tech and business circles)
Crisis management: Calm and innovative
Emergency preparedness: High
Legal knowledge: Medium
Financial literacy: Very high
Career aspirations: Pioneer in multiple fields
Job satisfaction: Very high
Work environment preference: High-tech and innovative
Managerial experience: Very high
Entrepreneurial tendency: Very high
Innovation capacity: Extremely high
Change management: Excellent
Project management skills: Very high
Cross-cultural skills: Medium
Global awareness: High
Travel experience: Very high
Language proficiency: English, basic Afrikaans
Dialect knowledge: None
Historical knowledge: Medium
Scientific literacy: Very high
Mathematical proficiency: Very high
Artistic ability: Low
Musical talent: Low
Creative writing: Low
Storytelling skills: Medium"""


users = {
    "user_0": USER_0, 
    "user_1": USER_1, 
    "user_2": USER_2, 
    "user_3": USER_3, 
    "user_4": USER_4,
    "user_5": USER_5,
    "user_6": USER_6,
    "user_7": USER_7,
    "user_8": USER_8,
    "user_9": USER_9, 
}

with open('data/users.json', 'w') as f:
    json.dump(users, f, indent=4)