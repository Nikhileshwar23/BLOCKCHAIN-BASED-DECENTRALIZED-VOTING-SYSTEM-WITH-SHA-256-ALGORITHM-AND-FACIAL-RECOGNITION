package net.codejava.controller;

import net.codejava.model.Candidate;
import net.codejava.repository.CandidateRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

@Controller
public class CandidateController {

    @Autowired
    private CandidateRepo candidateRepo;

    @GetMapping("/candidates")
    public String getCandidates(Model model) {
        List<Candidate> candidates = candidateRepo.findAll();
        model.addAttribute("candidates", candidates);
        return "candidates"; // Assuming you have a candidates.html template to display candidate data
    }
}
