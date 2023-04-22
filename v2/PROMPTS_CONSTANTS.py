WHAT_SHOULD_I_OBSERVE_PROMPT = "What should I observe?"
MEMORY_IMPORTANCE_PROMPT = "On the scale of 1 to 10, where 1 is purely mundane (e.g., brushing teeth, making bed) and 10 is extremely poignant (e.g., a break up, college acceptance), rate the likely poignancy of the following piece of memory.\n Memory: buying groceries at The Willows Market and Pharmacy\n Rating: <fill in>"
WHAT_SHOULD_I_REFLECT_ON_PROMPT = "Given only the information above, what are 3 most salient high-level questions we can answer about the subjects in the statements?"
CREATE_REFLECTION_PROMPT = "What 5 high-level insights can you infer from the above statements? (example format: insight (because of 1, 5, 3))"
BIOGRAPHICAL_MEMORY_1 = (
    "Meet Alice, a 25-year-old software developer from Chicago. Growing up in a family of engineers, Alice was always drawn to technology and coding. She earned her bachelor's degree in computer science from the University of Illinois and landed a job at a tech company in Silicon Valley. Alice is known for her problem-solving skills and attention to detail, which have earned her a reputation as a reliable and efficient developer. Outside of work, Alice enjoys hiking and exploring the outdoors, as well as reading science fiction novels. Her calm and composed demeanor helps her navigate through high-pressure situations both in her personal and professional life.",
    "She lives in San Francisco",
)  # biography: (natural language string, comprised of identity, occupation, and relationships)
