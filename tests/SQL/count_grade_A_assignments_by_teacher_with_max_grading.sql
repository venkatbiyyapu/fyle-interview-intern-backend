-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH TeacherGradingCount AS (
    SELECT 
        a.teacher_id,
        COUNT(a.id) AS graded_count
    FROM 
        assignments a
    WHERE 
        a.state = 'GRADED'
    GROUP BY 
        a.teacher_id
    ORDER BY 
        graded_count DESC
    LIMIT 1
)

SELECT 
    tgc.teacher_id,
    COUNT(a.id) AS grade_a_count
FROM 
    TeacherGradingCount tgc
JOIN 
    assignments a ON tgc.teacher_id = a.teacher_id
WHERE 
    a.grade = 'A'
GROUP BY 
    tgc.teacher_id;
