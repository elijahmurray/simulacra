WHAT_SHOULD_I_OBSERVE_PROMPT = (
    "What is this person doing right now?  (example format: [person's name] is [action]"
)
MEMORY_IMPORTANCE_PROMPT = "On the scale of 1 to 10, where 1 is purely mundane (e.g., brushing teeth, making bed) and 10 is extremely poignant (e.g., a break up, college acceptance), rate the likely poignancy of the following piece of memory.\n Memory: buying groceries at The Willows Market and Pharmacy\n Rating: <fill in>"
WHAT_SHOULD_I_REFLECT_ON_PROMPT = "Given only the information above, what are 3 most salient high-level questions we can answer about the subjects in the statements?"
CREATE_REFLECTION_PROMPT = "What 5 high-level insights can you infer from the above statements? (example format: insight (because of 1, 5, 3))"
BIOGRAPHICAL_MEMORY_1 = [
    "John Lin is a pharmacy shopkeeper at the Willow Market and Pharmacy who loves to help people. He is always looking for ways to make the process of getting medication easier for his customers; John Lin is living with his wife, Mei Lin, who is a college professor, and son, Eddy Lin, who is a student studying music theory; John Lin loves his family very much; John Lin has known the old couple next-door, Sam Moore and Jennifer Moore, for a few years; John Lin thinks Sam Moore is a kind and nice man; John Lin knows his neighbor, Yuriko Yamamoto, well; John Lin knows of his neighbors, Tamara Taylor and Carmen Ortiz, but has not met them before; John Lin and Tom Moreno are colleagues at The Willows Market and Pharmacy; John Lin and Tom Moreno are friends and like to discuss local politics together; John Lin knows the Moreno family somewhat well — the husband Tom Moreno and the wife Jane Moreno.",
    "John Lin is stretching",
]
BIOGRAPHICAL_MEMORY_2 = (
    "Meet Alice, a 25-year-old software developer from Chicago. Growing up in a family of engineers, Alice was always drawn to technology and coding. She earned her bachelor's degree in computer science from the University of Illinois and landed a job at a tech company in Silicon Valley. Alice is known for her problem-solving skills and attention to detail, which have earned her a reputation as a reliable and efficient developer. Outside of work, Alice enjoys hiking and exploring the outdoors, as well as reading science fiction novels. Her calm and composed demeanor helps her navigate through high-pressure situations both in her personal and professional life.",
    "She lives in San Francisco",
)  # biography: (natural language string, comprised of identity, occupation, and relationships)

WHAT_SHOULD_I_DO_NEXT_PROMPT = (
    "What should this person do next? (example format: [person's name] should [action])"
)
